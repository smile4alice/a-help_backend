import os

from flask_admin import form
from flask import url_for, Markup

from ahelp.admin.common import AdminModelView, file_path

DOCUMENTS = os.path.join(file_path, "ahelp", "static", "docs_and_reports")
os.makedirs(DOCUMENTS, exist_ok=True)


class DocsAndReportsAdminModelView(AdminModelView):
    column_list = [
        "photo_path",
        "statutes",
        "ownership_structure",
        "bank_account_holder_certificate",
        "certificate_of_nonprofit_organization",
        "extract_from_unified_state_register",
        "annual_report",
        "privacy_policy",
        "privacy_policy_en",
        "creation_date",
        "modification_date",
    ]
    column_labels = {
        "statutes": "Статут",
        "ownership_structure": "Структура власності",
        "photo_path": "Шлях до фото",
        "bank_account_holder_certificate": "Довідка про відкриття рахунку",
        "certificate_of_nonprofit_organization": "Довідка про присвоєння ознаки неприбутковості",
        "extract_from_unified_state_register": "Виписка з державного реєстру",
        "annual_report": "Звіт за рік",
        "privacy_policy": "Політика конфіденційності",
        "privacy_policy_en": "Політика конфіденційності",
        "creation_date": "Дата створення",
        "modification_date": "Дата змінення",
    }
    form_excluded_columns = [
        "creation_date",
        "modification_date",
    ]
    column_exclude_list = [
        "creation_date",
        "modification_date",
    ]
    fields = [
        {
            "name": "photo_path",
            "description": '''<span style="color: #007bff">
                              <b style="font-size: 14px">
                              Фото або PDF файл сертифікату.
                              </b></span>''',
        },
        {
            "name": "statutes",
            "description": '''<span style="color: #007bff">
                              <b style="font-size: 14px">
                              Файл статуту.
                              </b></span>''',
        },
        {
            "name": "ownership_structure",
            "description": '''<span style="color: #007bff">
                              <b style="font-size: 14px">
                              Файл структури власності.
                              </b></span>''',
        },
        {
            "name": "bank_account_holder_certificate",
            "description": '''<span style="color: #007bff">
                              <b style="font-size: 14px">
                              Файл довідки про відкриття рахунку.
                              </b></span>''',
        },
        {
            "name": "certificate_of_nonprofit_organization",
            "description": '''<span style="color: #007bff">
                              <b style="font-size: 14px">
                              Файл довідки про присвоєння ознаки неприбутковості.
                              </b></span>''',
        },
        {
            "name": "extract_from_unified_state_register",
            "description": '''<span style="color: #007bff">
                              <b style="font-size: 14px">
                              Файл виписки з державного реєстру.
                              </b></span>''',
        },
        {
            "name": "annual_report",
            "description": '''<span style="color: #007bff">
                              <b style="font-size: 14px">
                              Файл звіту за рік.
                              </b></span>''',
        },
        {
            "name": "privacy_policy",
            "description": '''<span style="color: #007bff">
                              <b style="font-size: 14px">
                              Файл політики конфіденційності Українською.
                              </b></span>''',
        },
        {
            "name": "privacy_policy_en",
            "description": '''<span style="color: #007bff">
                              <b style="font-size: 14px">
                              Файл політики конфіденційності Англійською.
                              </b></span>''',
        },
    ]

    def generate_image_name(model, file_data):
        return file_data.filename.replace(' ', '_')
    
    form_extra_fields = {}
    for field in fields:
        form_extra_fields[field["name"]] = form.FileUploadField("",
                                                                 base_path=DOCUMENTS,
                                                                 description=field["description"],
                                                                 namegen=generate_image_name)
    list_template = "admin/details_button.html"
    can_view_details = True
    details_modal = True

    def render(self, template, **kwargs):
        kwargs[
            "description"
        ] = """Файли можна завантажувати як в форматі фото, так у вигляді PDF
                документів. Якщо в таблиці міститься декілька записів,
                на сайті відображатиметься тільки один з них, останній по даті редагування."""
        return super(DocsAndReportsAdminModelView, self).render(template, **kwargs)

    def _list_thumbnail(column_name):
        def formatter(view, context, model, name):
            if not getattr(model, column_name):
                return ""
            url = url_for("static", filename=os.path.join(
                          "docs_and_reports/", getattr(model, column_name))
                )
            if getattr(model, column_name).split(".")[-1] in [
                "pdf", "csv", "txt", "doc", "DOCX", "html"
                ]:
                return Markup(f'<a href="{url}" target="_blank">{getattr(model, column_name)}</a>')
            
            elif getattr(model, column_name).split(".")[-1] in [
                "jpg", "jpeg", "png", "svg", "gif", "PNG"
                ]:
                return Markup(f'<img src={url} width="100">')

        return formatter

    column_formatters = {
        "photo_path": 
            _list_thumbnail("photo_path"),

        "statutes": 
            _list_thumbnail("statutes"),

        "ownership_structure": 
            _list_thumbnail("ownership_structure"),

        "bank_account_holder_certificate": 
            _list_thumbnail("bank_account_holder_certificate"),

        "certificate_of_nonprofit_organization": 
            _list_thumbnail("certificate_of_nonprofit_organization"),

        "extract_from_unified_state_register": 
            _list_thumbnail("extract_from_unified_state_register"),

        "annual_report": 
            _list_thumbnail("annual_report"),

        "privacy_policy": 
            _list_thumbnail("privacy_policy"),

        "privacy_policy_en": 
            _list_thumbnail("privacy_policy_en"),

        "creation_date": 
            lambda view, context, model, name: model.creation_date.strftime("%d %B %Y %H:%M:%S"),

        "modification_date": 
            lambda view, context, model, name: model.modification_date.strftime("%d %B %Y %H:%M:%S")
        if model.modification_date
        else "",
    }
