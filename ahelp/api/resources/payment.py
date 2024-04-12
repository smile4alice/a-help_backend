from datetime import datetime
from re import sub as re_sub

from dateutil.relativedelta import relativedelta
from flask_restful import Resource, abort
from flask import request, redirect, current_app
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from cloudipsp import Checkout, Api as FondyApi
from paypalrestsdk import (
    configure as paypal_config,
    BillingPlan,
    BillingAgreement,
    Payment as PayPalPayment,
)

from ahelp.models import PaymentDetailsModel, PaymentDetailsModel, PaymentModel
from ahelp.api.schemas import PaymentDetailsSchema


class PaymentResource(Resource):
    """
    A resource for managing payment-related operations.

    ---
    get:
        tags:
            - api
        description: Retrieves payment details.
        parameters:
            - in: path
              name: language
              schema:
                type: string
              description: Language of the header, body, title, and description fields.
              default: empty
              example: en
        responses:
            200:
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                payment_details:
                                    type: array
                                    items:
                                        $ref: '#/components/schemas/PaymentDetailsSchema'
                                header:
                                    type: string
                                    description: Page header "How can you help".
                                body:
                                    type: string
                                    description: call for help.
                                title:
                                    type: string
                                    description: The help details title.
                                description:
                                    type: string
                                    description: Description above the payment buttons.
                                photo_path:
                                    type: string
                                    description: Picture on the page as you can help.
    post:
        tags:
            - api
        summary: Create a new payment.
        description: |
            Creates a new payment for the specified payment service. The type of payment
            and its details must be provided in the request body.
        parameters:
            - name: payment_data
              in: body
              description: The payment data to use for creating the payment.
              schema:
                    type: object
                    properties:
                        payment_service:
                            type: string
                            description: The payment service to use for creating the payment.
                            enum: [FONDY, PAYPAL]
                        payment_type:
                            type: string
                            description: The type of payment, which will be used to create the payment.
                            enum: [ONE-OFF, RECCURING]
                        amount:
                            type: object
                            properties:
                                total:
                                    type: string
                                    description: The total amount for the payment.
                                currency:
                                    type: string
                                    description: The currency for the payment.
                            description: The payment amount details.
                        description:
                            type: string
                            description: The payment description.
                        payment_definitions:
                            description: The payment definition details.
                            type: object
                            properties:
                                frequency:
                                    type: string
                                    description: Unit of time between each payment
                                frequency_interval:
                                    type: string
                                    description: Payment frequency (every 1/2/3/5...N days etc.)
                                cycles:
                                    type: string
                                    description: The number of charges after which the subscription will be canceled.
        responses:
            200:
                description: OK
                content:
                    application/json:
                        schema:
                            type: string
                            description: |
                                URL of the payment page. For PayPal, this is the URL of the approval
                                page where the user must approve the payment. For Fondy, this is the URL
                                of the payment page where the user must enter payment information.
                            example: "https://www.paypal.com/cgi-bin/webscr?cmd=_express-checkout&token=EC-8XA12210UB957233U"
                    application/x-www-form-urlencoded:
                        schema:
                            type: string
                            description: |
                                If the visitor successfully pays redirects to the home page, additionally
                                the parameter "success_payment=True" is returned
                            example: "https://www.success_payment_link/hero?success=True"
            400:
                description: ValueError or KeyError when receiving data from the server
            404:
                description: No payment data found
            500:
                description: All related errors related to payment data validation and ValidationError, AttributeError or Unexpected error when transmitting data from the server.
    """

    method_decorators = [jwt_required()]

    def get(self, language=None):
        try:
            payment_details_data = PaymentDetailsModel.query.limit(3).all()
            payment_data = PaymentModel.query.order_by(PaymentModel.creation_date.asc()).first_or_404(
                description="Payment block data not found"
            )
            payment_schema = PaymentDetailsSchema(many=True)
            header = "header_en" if language == "en" else "header"
            body = "body_en" if language == "en" else "body"
            title = "title_en" if language == "en" else "title"
            description = "description_en" if language == "en" else "description"
            return {
                "payment_details": payment_schema.dump(payment_details_data),
                "header": getattr(payment_data, header, None),
                "body": getattr(payment_data, body, None),
                "title": getattr(payment_data, title, None),
                "description": getattr(payment_data, description, None),
                "photo_path": f"{current_app.config.get('BASE_URL')}/static/payment/{getattr(payment_data, 'photo_path', None)}",
            }
        except ValidationError as e:
            abort(500, error=f"ValidationError: {str(e)}")
        except AttributeError as e:
            abort(500, error=f"AttributeError: {str(e)}")
        except ValueError as e:
            abort(400, error=f"ValueError: {str(e)}")
        except KeyError as e:
            abort(400, error=f"KeyError: {str(e)}")
        except Exception as e:
            abort(500, error=f"Unexpected error: {str(e)}")

    def post(self):
        try:
            json_data = request.get_json()
            if json_data["payment_service"] == "FONDY":
                return self.create_fondy_payment(
                    json_data, current_app.config.get("FONDY_MERCHANT_ID"), current_app.config.get("FONDY_SECRET_KEY")
                )

            elif json_data["payment_service"] == "PAYPAL":
                validate_paypal_data(json_data)
                self.configure_paypal_client(
                    current_app.config.get("PAYPAL_MODE"),
                    current_app.config.get("PAYPAL_CLIENT_ID"),
                    current_app.config.get("PAYPAL_CLIENT_SECRET"),
                )
                if json_data["payment_type"] == "ONE-OFF":
                    return self.create_paypal_one_off_payment(json_data)
                else:
                    return self.create_paypal_subscription(json_data)
        except ValidationError as e:
            abort(500, error=f"ValidationError: {str(e)}")
        except AttributeError as e:
            abort(500, error=f"AttributeError: {str(e)}")
        except ValueError as e:
            abort(400, error=f"ValueError: {str(e)}")
        except KeyError as e:
            abort(400, error=f"KeyError: {str(e)}")
        except Exception as e:
            abort(500, error=f"Unexpected error: {str(e)}")

    @classmethod
    def configure_paypal_client(cls, mode, client_id, client_secret):
        return paypal_config(
            {
                "mode": mode,
                "client_id": client_id,
                "client_secret": client_secret,
            }
        )

    @classmethod
    def create_paypal_one_off_payment(cls, json_data):
        base_url = current_app.config.get("BASE_URL")
        cancel_url = current_app.config.get("PAYPAL_CANCEL_URL")
        total_of_amount = cls.validate_total_of_amount(json_data["amount"]["total"])
        payment = PayPalPayment(
            {
                "intent": "sale",
                "payer": {"payment_method": "paypal"},
                "redirect_urls": {
                    "return_url": f"{base_url}/api/v1/handlers/payment/paypal/execute",
                    "cancel_url": f"{cancel_url}?success_payment=FALSE",
                },
                "transactions": [
                    {
                        "item_list": {
                            "items": [
                                {
                                    "name": "Payment for A-HELP",
                                    "description": json_data["description"],
                                    "price": total_of_amount,
                                    "currency": json_data["amount"]["currency"],
                                    "quantity": 1,
                                }
                            ]
                        },
                        "amount": {
                            "total": total_of_amount,
                            "currency": json_data["amount"]["currency"],
                        },
                        "description": json_data["description"],
                    }
                ],
            }
        )
        if payment.create():
            for link in payment.links:
                if link.method == "REDIRECT":
                    return link.href
        else:
            abort(500, error=payment.error)

    @classmethod
    def create_paypal_subscription(cls, json_data):
        base_url = current_app.config.get("BASE_URL")
        cancel_url = current_app.config.get("PAYPAL_CANCEL_URL")
        total_of_amount = cls.validate_total_of_amount(json_data["amount"]["total"])
        billing_plan_attributes = {
            "name": "Subscribes plan for A-HELP",
            "description": json_data["description"],
            "type": json_data["payment_definitions"]["type"],
            "merchant_preferences": {
                "return_url": f"{base_url}/api/v1/handlers/payment/paypal/execute",
                "cancel_url": f"{cancel_url}?success_payment=FALSE",
                "max_fail_attempts": "0",
                "initial_fail_amount_action": "continue",
                "auto_bill_amount": "yes",
                "setup_fee": {
                    "currency": json_data["amount"]["currency"],
                    "value": total_of_amount,
                },
            },
            "payment_definitions": [
                {
                    "name": "Subscribes for A-HELP",
                    "type": "REGULAR",
                    "frequency": json_data["payment_definitions"]["frequency"],
                    "frequency_interval": json_data["payment_definitions"]["frequency_interval"],
                    "cycles": json_data["payment_definitions"]["cycles"],
                    "amount": {
                        "currency": json_data["amount"]["currency"],
                        "value": total_of_amount,
                    },
                }
            ],
        }
        billing_plan = BillingPlan(billing_plan_attributes)
        if not billing_plan.create() or not billing_plan.activate():
            abort(500, error=billing_plan.error)
        frequency_interval = json_data["payment_definitions"]["frequency_interval"]
        now = datetime.now()
        match json_data["payment_definitions"]["frequency"]:
            case "DAY":
                start_date = now + relativedelta(days=frequency_interval)
            case "WEEK":
                start_date = now + relativedelta(weeks=frequency_interval)
            case "MONTH":
                start_date = now + relativedelta(months=frequency_interval)
            case "YEAR":
                start_date = now + relativedelta(years=frequency_interval)

        billing_agreement = BillingAgreement(
            {
                "name": "Billing Agreement",
                "description": "Agreement for" + json_data["description"],
                "start_date": start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "plan": {"id": billing_plan.id},
                "payer": {"payment_method": "paypal"},
            }
        )
        if not billing_agreement.create():
            abort(500, error=billing_agreement.error)
        for link in billing_agreement.links:
            if link.rel == "approval_url":
                return link.href

    @classmethod
    def create_fondy_payment(cls, json_data, fondy_merchant_id, fondy_secret_key):
        base_url = current_app.config.get("BASE_URL")
        fondy_api = FondyApi(merchant_id=fondy_merchant_id, secret_key=fondy_secret_key)
        checkout = Checkout(api=fondy_api)
        total_of_amount = cls.validate_total_of_amount(json_data["amount"]["total"]).replace(".", "")
        data = {
            "amount": total_of_amount,
            "currency": json_data["amount"]["currency"],
            "order_desc": json_data["description"],
            "subscription": "N" if json_data["payment_type"] == "ONE-OFF" else "Y",
            "lifetime": 600,
            "response_url": f"{base_url}/api/v1/handlers/payment/fondy/execute",
        }
        return checkout.url(data)["checkout_url"]

    def validate_total_of_amount(total: str) -> str:
        total = re_sub(r"[,.]", ".", total)
        if "." not in total:
            total += ".00"
        else:
            total = total.split(".")[0] + "." + total.split(".")[1].ljust(2, "0")[:2]
        return total


def validate_paypal_data(json_data: dict) -> str:
    interval_error = "Interval greater than 12 months."
    example = """Correct format:
    {"payment_service": "PAYPAL", "payment_type": "RECURRING",
    "description": "TEST DONATE", "amount": {"total": "300.25", "currency": "USD"},
    "payment_definitions": {"type": "FIXED", "frequency": "WEEK", "frequency_interval": "2", "cycles": "1"}"""
    if not isinstance(json_data, dict):
        abort(500, error=example)
    elif json_data["payment_type"] != "ONE-OFF" and json_data["payment_type"] != "RECURRING":
        abort(500, error="Only two payment types are available: < ONE-OFF > and < RECURRING > ")
    elif json_data["payment_type"] == "RECURRING":
        frequency_interval = int(json_data["payment_definitions"]["frequency_interval"])
        frequency = json_data["payment_definitions"]["frequency"]
        if frequency == "DAY" and frequency_interval > 365:
            abort(500, error=interval_error)
        elif frequency == "WEEK" and frequency_interval > 52:
            abort(500, error=interval_error)
        elif frequency == "MONTH" and frequency_interval > 12:
            abort(500, error=interval_error)
        elif frequency == "YEAR" and frequency_interval > 1:
            abort(500, error=interval_error)
        cycles = int(json_data["payment_definitions"]["cycles"])
        payment_method = json_data["payment_definitions"]["type"]
        if payment_method == "FIXED" and cycles < 1:
            abort(500, error="If you select <FIXED>, then the cycles must be > 0")
        elif payment_method == "INFINITE" and cycles != 0:
            abort(500, error="If you select <INFINITE>, then the cycles must be == 0")
        elif payment_method != "FIXED" and payment_method != "INFINITE":
            abort(500, error="Only two payment modes are available: < FIXED > and < INFINITE > ")


class SuccessFondyResource(Resource):
    def post(self):
        success_payment_link = current_app.config.get("MAIN_PAGE_URL")
        payer_info = request.form.to_dict()
        if payer_info["order_status"] == "approved":
            current_app.logger.warning(
                f"""order_id: {payer_info['order_id']},
                    sender_email: {payer_info['sender_email']},
                    amount: {payer_info['amount']},
                    currency: {payer_info['currency']},"""
            )
        return redirect(f"{success_payment_link}?success_payment=True")


class SuccessPayPalResource(Resource):
    def get(self):
        success_payment_link = current_app.config.get("MAIN_PAGE_URL")
        get_data = request.args
        if payment_id := get_data.get("paymentId", None):
            payment = PayPalPayment.find(payment_id)
            if payment.execute({"payer_id": get_data.get("PayerID")}):
                payment_data = payment.to_dict()
                payer_info = payment_data["payer"]["payer_info"]
                amount = payment_data["transactions"][0]["amount"]
                amount_result = f"[{amount['total']} {amount['currency']}]"
                current_app.logger.warning(
                    f"""PayPal successfully: {payment_data['intent']} [{payment_data['id']}] with {amount_result}
                    \t\t\t from payer_id: [{payer_info['payer_id']}]
                    \t\t\t email: [{payer_info['email']}] country: [{payer_info['country_code']}]"""
                )
            else:
                current_app.logger.error(payment.error)
        else:
            billing_data = BillingAgreement.execute(get_data.get("token", "")).to_dict()
            payer_info = billing_data["payer"]["payer_info"]
            plan_def = billing_data["plan"]["payment_definitions"][0]
            plan_data = f"[{billing_data['id']}] with [{plan_def['amount']['value']} {plan_def['amount']['currency']}]"
            payment = f"[{plan_def['frequency_interval']} {plan_def['frequency']} {plan_def['type']} {'INFINITE' if int(plan_def['cycles']) > 0 else 'FIXED'}]"
            current_app.logger.warning(
                f"""PayPal successfully: {payment} 
                \t\t\t plan {plan_data} 
                \t\t\t from payer_id: [{payer_info['payer_id']}]
                \t\t\t email: [{payer_info['email']}] 
                \t\t\t country: [{payer_info['shipping_address']['country_code']}]"""
            )
        return redirect(f"{success_payment_link}?success_payment=True")
