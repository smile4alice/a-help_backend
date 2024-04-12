import uuid
import os

from flask_admin import form
from flask import url_for, Markup

from ahelp.admin.common import AdminModelView, file_path


class OurTeamAdminModelView(AdminModelView):
    column_list = [
        "founder",
        "photo_path",
        "name",
        "name_en",
        "description",
        "description_en",
        "creation_date",
        "modification_date",
    ]
    column_labels = {
        "founder": "Засновник",
        "photo_path": "Фотографія",
        "name": "Ім'я",
        "name_en": "Ім'я(EN)",
        "description": "Опис",
        "description_en": "Опис(EN)",
        "creation_date": "Дата створення",
        "modification_date": "Дата змінення",
    }
    column_descriptions = dict(
        founder='Може бути тільки один. Відображатиметься першим на сторінці "Наша команда"',
        name="Прізвище та ім'я для Українських відвідувачів сайту",
        name_en="Прізвище та ім'я для зарубіжних відвідувачів сайту",
        description="Опис діяльності, який відображатиметься для Українських відвідувачів сайту",
        description_en="Опис діяльності, який відображатиметься для зарубіжних відвідувачів сайту",
    )
    form_excluded_columns = (
        "modification_date",
        "creation_date",
    )
    column_searchable_list = [
        "name",
        "name_en",
    ]
    column_choices = {
        "founder": [
            (True, "Так"),
            (False, "Ні"),
        ]
    }
    column_default_sort = [
        ("founder", True),
        ("id", False),
    ]
    column_editable_list = [
        "founder",
        "name",
        "name_en",
    ]
    column_exclude_list = [
        "creation_date",
        "modification_date",
    ]
    can_set_page_size = True
    can_view_details = True
    details_modal = True
    list_template = "admin/details_button.html"

    def render(self, template, **kwargs):
        kwargs[
            "description"
        ] = '''Якщо в полі "Засновник" напроти профілю поставити галочку,
               профіль відображатиметься першим на сторінці "Наша команда".
               Будьте уважні, засновник або директор фонду може бути лише один.'''
        return super(OurTeamAdminModelView, self).render(template, **kwargs)

    def _list_thumbnail(size=100):
        def thumbnail_formatter(view, context, model, name):
            if not model.photo_path:
                return ""
            url = url_for("static", filename=os.path.join("/our_team/", model.photo_path))
            if model.photo_path.split(".")[-1] in ["jpg", "jpeg", "png", "svg", "gif"]:
                return Markup(f"<img src={url} width={size}>")
        return thumbnail_formatter

    def generate_image_name(model, file_data):
        return f'{uuid.uuid4().hex[:16]}.{file_data.filename.split(".")[-1]}'

    def validate_directory(form, field):
        upload_folder = os.path.join(file_path, "ahelp", "static", "our_team")
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
            "Виберіть фото партнера",
            base_path=os.path.join(file_path, "ahelp", "static", "our_team"),
            url_relative_path="our_team/",
            namegen=generate_image_name,
            allowed_extensions=["jpg", "png", "jpeg", "gif"],
            max_size=(1200, 780, True),
            thumbnail_size=(100, 100, True),
            validators=[validate_directory],
        )
    }
