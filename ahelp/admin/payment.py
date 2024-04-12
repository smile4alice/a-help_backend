import uuid
import os

from wtforms import TextAreaField
from flask_admin import form
from flask import url_for, Markup

from ahelp.admin.common import AdminModelView, file_path


class PaymentAdminModelView(AdminModelView):
    column_list = [
        "photo_path",
        "header",
        "header_en",
        "body",
        "body_en",
        "title",
        "title_en",
        "description",
        "description_en",
        "creation_date",
        "modification_date",
    ]
    column_labels = {
        "id": "ID",
        "photo_path": "Шлях до фото",
        "header": '"Шапка" сторінки',
        "header_en": '"Шапка" сторінки(EN)',
        "body": "Короткий опис",
        "body_en": "Короткий опис(EN)",
        "title": "Заголовок",
        "title_en": "Заголовок(EN)",
        "description": "Заклик до допомоги",
        "description_en": "Заклик до допомоги",
        "creation_date": "Дата створення",
        "modification_date": "Дата змінення",
    }
    form_excluded_columns = (
        "modification_date",
        "creation_date",
    )
    form_columns = (
        "header",
        "header_en",
        "body",
        "body_en",
        "title",
        "title_en",
        "description",
        "description_en",
        "photo_path",
    )
    column_descriptions = dict(
        header='"Шапка" строрінки "Як ви можете допомогти".',
        header_en="'Шапка' сторінки англійською.",
        body="Стислий опис, як людина може допомогти.",
        body_en="Стислий опис, як людина може допомогти (для іноземних відвідувачів сайту).",
        title="Гасло до донату. Відображається над кнопками оплати.",
        title_en="Гасло до донату англійською. Відображається над кнопками оплати",
        description="Загальний заклик до допомоги. Відображається над кнопками оплати.",
        description_en="Загальний заклик до допомоги англійською. Відображається над кнопками оплати.",
    )
    column_exclude_list = [
        "id",
        "creation_date",
        "modification_date",
    ]
    column_editable_list = (
        "header",
        "header_en",
        "title",
        "title_en",
    )
    can_set_page_size = True
    can_view_details = True
    details_modal = True
    list_template = "admin/details_button.html"

    def render(self, template, **kwargs):
        kwargs[
            "description"
        ] = '''На сторінці "Як Ви можете допомогти"
               відображатиметься тільки один запис,
               останній по даті додавання або редагування.'''
        return super(PaymentAdminModelView, self).render(template, **kwargs)

    def _list_thumbnail(size = 100):
        def thumbnail_formatter(view, context, model, name):
            if not model.photo_path:
                return ""
            url = url_for("static", filename=os.path.join("/payment/", model.photo_path))
            if model.photo_path.split(".")[-1] in ["jpg", "jpeg", "png", "svg", "gif"]:
                return Markup(f'<img src={url} width={size}>')
        return thumbnail_formatter

    def generate_image_name(model, file_data):
        return f'{uuid.uuid4().hex[:16]}.{file_data.filename.split(".")[-1]}'

    def validate_directory(form, field):
        upload_folder = os.path.join(file_path, "ahelp", "static", "payment")
        os.makedirs(upload_folder, exist_ok=True)

    column_formatters = {"photo_path": _list_thumbnail()}
    column_formatters_detail = {
        "photo_path": _list_thumbnail(300),
        "creation_date":
            lambda view, context, model, name: model.creation_date.strftime("%d %B %Y %H:%M:%S"),
        "modification_date":
            lambda view, context, model, name: model.modification_date.strftime("%d %B %Y %H:%M:%S")
        if model.modification_date
        else "",
    }
    form_extra_fields = {
        "photo_path": form.ImageUploadField(
            "",
            base_path=os.path.join(file_path, "ahelp", "static", "payment"),
            url_relative_path="/payment/",
            namegen=generate_image_name,
            allowed_extensions=["jpg", "png", "jpeg", "gif"],
            max_size=(1200, 780, True),
            thumbnail_size=(100, 100, True),
            validators=[validate_directory],
            description='''<span style="color: #007bff">
                           <b style="font-size: 14px">
                           Виберіть фото для розділу донатів</b></span>''',
        ),
        "body": TextAreaField(
            "Короткий опис",
            render_kw={
                "class": "form-control",
                "rows": 3,
                "style": "border: 0.5px solid #007bff"
                }
        ),
        "body_en": TextAreaField(
            "Короткий опис (EN)",
            render_kw={
                "class": "form-control",
                "rows": 3,
                "style": "border: 0.5px solid #007bff"
                }
        ),
        "description": TextAreaField(
            "Заклик до допомоги",
            render_kw={
                "class": "form-control",
                "rows": 3,
                "style": "border: 0.5px solid #007bff"
                }
        ),
        "description_en": TextAreaField(
            "Заклик до допомоги (EN)",
            render_kw={
                "class": "form-control",
                "rows": 3,
                "style": "border: 0.5px solid #007bff"
                }
        ),
    }
