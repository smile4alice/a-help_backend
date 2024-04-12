from ahelp.admin.common import AdminModelView


class PaymentDetailsAdminModelView(AdminModelView):
    column_list = [
        "currency",
        "company_name",
        "iban_code",
        "name_of_bank",
        "bank_address",
        "edrpou_code",
        "swift_code",
        "company_address",
        "correspondent_bank",
        "address_of_correspondent_bank",
        "account_of_the_correspondent_bank",
        "swift_code_of_the_correspondent_bank",
        "creation_date",
        "modification_date",
    ]
    column_labels = {
        "currency": "Тип валюти",
        "company_name": "Назва компанії",
        "iban_code": "IBAN код",
        "name_of_bank": "Назва банку",
        "bank_address": "Адреса банку",
        "edrpou_code": "КОД ЄДРПОУ",
        "swift_code": "SWIFT код",
        "company_address": "Адреса компанії",
        "correspondent_bank": "Банк кореспондент",
        "address_of_correspondent_bank": "Адреса банку кореспондента",
        "account_of_the_correspondent_bank": "Рахунок в банку кореспонденті",
        "swift_code_of_the_correspondent_bank": "SWIFT код банку кореспондента",
        "creation_date": "Дата створення",
        "modification_date": "Дата змінення",
    }
    form_excluded_columns = (
        "modification_date",
        "creation_date",
    )
    column_editable_list = [
        "currency",
        "company_name",
        "iban_code",
        "name_of_bank",
        "bank_address",
        "edrpou_code",
        "swift_code",
        "company_address",
        "correspondent_bank",
        "address_of_correspondent_bank",
        "account_of_the_correspondent_bank",
        "swift_code_of_the_correspondent_bank",
    ]
    column_descriptions = dict(
        currency="Тип валюти, реквізити для оплати якою вказуються.",
        company_name="""Повна назва фонду. Відображатиметься в випадаючому меню,
                        якщо користувач обере оплату за реквізитами""",
        company_address="Адреса вашого фонду.",
        iban_code="Від 29 до 34 символів. (В Україні 29 символів).",
        edrpou_code="8 цифр.",
        swift_code="Від 8 до 11 символів.",
        swift_code_of_the_correspondent_bank="Від 8 до 11 символів.",
    )
    form_choices = {
        "currency": [
            ("UAH", "UAH"),
            ("EUR", "EUR"),
            ("USD", "USD"),
        ]
    }
    column_searchable_list = [
        "iban_code",
        "edrpou_code",
        "swift_code",
        "swift_code_of_the_correspondent_bank",
    ]
    column_exclude_list = [
        "id",
        "creation_date",
        "modification_date",
    ]
    column_formatters = {
        "creation_date":
            lambda view, context, model, name: model.creation_date.strftime("%d %B %Y %H:%M:%S"),
        "modification_date":
            lambda view, context, model, name: model.modification_date.strftime("%d %B %Y %H:%M:%S")
        if model.modification_date
        else "",
    }
    can_view_details = True
    details_modal = True
    list_template = "admin/details_button.html"

    def render(self, template, **kwargs):
        kwargs[
            "description"
        ] = """Будьте уважні при виборі типу валюти та вводі реквізитів,
               вони відображатимуться коли користувачі оберуть оплату
               за реквізитами. На сайті відображатимуться лише перші три
               записи з таблиці реквізитів. Якщо записів більше ніж три,
               на сторінці відображатимуться перші по даті редагування."""
        return super(PaymentDetailsAdminModelView, self).render(template, **kwargs)
