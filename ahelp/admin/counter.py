from ahelp.admin.common import AdminModelView


class CounterAdminModelView(AdminModelView):
    column_list = [
        "currency_symbol",
        "amount",
        "locale",
        "creation_date",
        "modification_date",
    ]
    column_labels = {
        "currency_symbol": "Валюта (USD, EUR, UAH)",
        "amount": "Сума",
        "locale": "Locale (для різних регіонів (en_US, en_EU, uk_UA))",
        "creation_date": "Дата створення",
        "modification_date": "Дата змінення",
    }
    column_editable_list = ["currency_symbol", "locale", "amount"]
    form_excluded_columns = (
        "modification_date",
        "creation_date",
    )
    form_choices = {
        "currency_symbol":
            [
                ("UAH", "UAH"),
                ("EUR", "EUR"),
                ("USD", "USD"),
            ],
        "locale": 
            [
                ("en_US", "en_US"),
                ("en_EU", "en_EU"),
                ("uk_UA", "uk_UA"),
            ]
        }
    column_exclude_list = ["creation_date"]
    column_formatters = {
        "modification_date":
            lambda view, context, model, name: model.modification_date.strftime("%d %B %Y %H:%M:%S")
        if model.modification_date else "",
        "creation_date":
            lambda view, context, model, name: model.creation_date.strftime("%d %B %Y %H:%M:%S"),
    }
