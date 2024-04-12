from datetime import datetime

from marshmallow import validate

from ahelp.models import PaymentDetailsModel
from ahelp.extensions import ma, db


class PaymentDetailsSchema(ma.SQLAlchemyAutoSchema):
    id: int = ma.Integer(dump_only=True)
    currency: str = ma.String(required=True, validate=validate.OneOf(choices=["EUR", "USD", "UAH"]))
    company_name: str = ma.String(required=True, validate=validate.Length(min=5, max=100))
    iban_code: str = ma.String(required=True, validate=validate.Length(min=29, max=34))
    name_of_bank: str = ma.String(required=True, validate=validate.Length(min=5, max=200))
    bank_address: str = ma.String(required=True, validate=validate.Length(min=5, max=200))
    edrpou_code: int = ma.String(required=True, validate=validate.Length(equal=8))
    swift_code: str = ma.String(required=True, validate=validate.Length(min=8, max=11))
    company_address: str = ma.String(required=True, validate=validate.Length(min=5, max=200))
    correspondent_bank: str = ma.String(validate=validate.Length(min=5, max=200))
    address_of_correspondent_bank: str = ma.String(validate=validate.Length(min=5, max=200))
    account_of_the_correspondent_bank: str = ma.String(validate=validate.Length(min=5, max=200))
    swift_code_of_the_correspondent_bank: str = ma.String(validate=validate.Length(min=8, max=11))
    creation_date: datetime = ma.DateTime(dump_only=True)
    modification_date: datetime = ma.DateTime(dump_only=True)

    class Meta:
        model = PaymentDetailsModel
        sqla_session = db.session
        load_instance = True
