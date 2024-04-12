import uuid
import os

from flask_admin import form
from wtforms import TextAreaField
from flask import Markup, url_for

from ahelp.admin.common import AdminModelView, file_path


class ContactsAdminModelView(AdminModelView):


    column_list = [
        "photo_path",
        "google_maps",
        "address",
        "address_en",
        "email",
        "number",
        "facebook",
        "instagram",
        "telegram",
        "viber",
        "creation_date",
        "modification_date",
    ]
    column_labels = {
        "photo_path": "Фото",
        "google_maps": "HTML код GoogleMaps",
        "address": "Адреса",
        "address_en": "Адреса(EN)",
        "email": "Email",
        "number": "Телефон",
        "facebook": "Facebook",
        "instagram": "Instagram",
        "telegram": "Telegram",
        "viber": "Viber",
        "creation_date": "Дата створення",
        "modification_date": "Дата змінення",
    }
    form_columns = (
        "number",
        "email",
        "address",
        "address_en",
        "facebook",
        "instagram",
        "telegram",
        "viber",
        "google_maps",
        "photo_path",
    )
    column_editable_list = [
        "number",
        "email",
        "address",
        "address_en",
        "facebook",
        "instagram",
        "telegram",
        "viber",
    ]
    form_excluded_columns = [
        "creation_date",
        "modification_date",
    ]
    column_exclude_list = [
        "creation_date",
        "modification_date",
    ]
    can_view_details = True
    details_modal = True
    list_template = "admin/details_button.html"

    def render(self, template, **kwargs):
        kwargs[
            "description"
        ] = """
<p>Щоб отримати посилання на гугл карту з координатами вашого фонду, Вам потрібно:</p>
<ol>
  <li>
    <p>Зайти в Google Maps та ввести адресу фонду в пошук.</p>
    <img src="/static/interface/g_maps/find_string.jpg" alt="Крок 1" style="max-width: 300px; border-radius: 10px;">
  </li>
  <li>
    <p>Перейти в меню (кнопка зліва, в пошуковому рядку) та натиснути 'Вставити карту або поділитися'.</p>
    <img src="/static/interface/g_maps/map.jpg" alt="Крок 2" style="max-width: 300px; border-radius: 10px;">
  </li>
  <li>
    <p>В спливаючому вікні обрати вкладку 'Вставити карту' і переключити в лівому нижньому кутку тип карти на той, який Вам подобається більше.</p>
    <img src="/static/interface/g_maps/share_map.jpg" alt="Крок 3" style="max-width: 300px; border-radius: 10px;">
  </li>
  <li>
    <p>Після цього потрібно скопіювати HTML код над картою та вставити в відповідне поле в таблиці 'Контакти'.</p>
    <img src="/static/interface/g_maps/code.jpg" alt="Крок 4" style="max-width: 300px; border-radius: 10px;">
  </li>
</ol>
<p>Якщо після цього в таблиці відображається інтерактивна карта з адресою Вашого фонду, значить Ви все зробили правильно.</p>
"""
        return super(ContactsAdminModelView, self).render(template, **kwargs)

    def _list_thumbnail(size=100):
        def thumbnail_formatter(view, context, model, name):
            if not model.photo_path:
                return ""
            url = url_for("static", filename=os.path.join("/contacts/", model.photo_path))
            if model.photo_path.split(".")[-1] in ["jpg", "jpeg", "png", "svg", "gif"]:
                return Markup(f"<img src={url} width={size}>")
        return thumbnail_formatter

    def generate_image_name(model, file_data):
        return f'{uuid.uuid4().hex[:16]}.{file_data.filename.split(".")[-1]}'

    def validate_directory(form, field):
        upload_folder = os.path.join(file_path, "ahelp", "static", "contacts")
        os.makedirs(upload_folder, exist_ok=True)

    form_extra_fields = {
        "photo_path": form.ImageUploadField(
            "",
            base_path=os.path.join(file_path, "ahelp", "static", "contacts"),
            url_relative_path="/contacts/",
            namegen=generate_image_name,
            allowed_extensions=["jpg", "jpeg", "png", "svg", "gif"],
            max_size=(1200, 780, True),
            thumbnail_size=(100, 100, True),
            validators=[validate_directory],
            description='''<span style="color: #007bff">
                           <b style="font-size: 14px">
                            Photo for the site footer</b></span>''',
        ),
        "google_maps": TextAreaField(
            "HTML код GoogleMaps",
            render_kw={
                "class": "form-control",
                "rows": 3,
                "style": "border: 0.5px solid #007bff"
            }
        ),
    }
    column_formatters = {
        "google_maps": lambda v, c, m, p: Markup(
            f'''<span style="display:inline-block;
                 max-width:200px;max-height:200px;
                 overflow:hidden;white-space:nowrap;
                 text-overflow:ellipsis;">{m.google_maps}</span>'''
        ),
        "photo_path": _list_thumbnail(200),
    }
    column_formatters_detail = {
        "photo_path": _list_thumbnail(200),
        "google_maps": lambda v, c, m, p: Markup(
            (
                f'''<span style="display:inline-block;
                     max-width:100%;max-height:500px;
                     overflow:hidden;white-space:nowrap;
                     text-overflow:ellipsis;">{m.google_maps}</span>'''
            )
        ),
        "creation_date":
            lambda view, context, model, name: model.creation_date.strftime("%d %B %Y %H:%M:%S"),
        "modification_date":
            lambda view, context, model, name: model.modification_date.strftime("%d %B %Y %H:%M:%S")
        if model.modification_date
        else "",
    }
