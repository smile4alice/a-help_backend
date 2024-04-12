import uuid
import os

from flask_admin import form
from flask import url_for, Markup

from ahelp.admin.common import AdminModelView, file_path


class GoalsFoundationAdminModelView(AdminModelView):
    column_list = [
        "photo_path",
        "title",
        "title_en",
        "description",
        "description_en",
        "creation_date",
        "modification_date",
    ]
    column_labels = {
        "photo_path": "Фотографія",
        "title": "Заголовок",
        "title_en": "Заголовок(EN)",
        "description": "Опис",
        "description_en": "Опис(EN)",
        "creation_date": "Дата створення",
        "modification_date": "Дата змінення",
    }
    form_excluded_columns = (
        "modification_date",
        "creation_date",
    )
    column_descriptions = dict(
        description="Опис до карточок на сторінці історії фонду.",
        description_en="Опис до карточок на сторінці історії фонду англійською.",
    )
    column_exclude_list = [
        "creation_date",
        "modification_date",
    ]
    column_editable_list = [
        "title",
        "title_en",
    ]
    can_view_details = True
    details_modal = True

    def _list_thumbnail(size = 100):
        def thumbnail_formatter(view, context, model, name):
            if not model.photo_path:
                return ""
            url = url_for("static", filename=os.path.join("/goals_foundation/",
                                                           model.photo_path))
            if model.photo_path.split(".")[-1] in [
                "jpg", "jpeg", "png", "svg", "gif"
                ]:
                return Markup(f'<img src={url} width={size}>')
        return thumbnail_formatter

    def generate_image_name(model, file_data):
        return f'{uuid.uuid4().hex[:16]}.{file_data.filename.split(".")[-1]}'

    def validate_directory(form, field):
        upload_folder = os.path.join(file_path, "ahelp", "static", "goals_foundation")
        os.makedirs(upload_folder, exist_ok=True)

    column_formatters = {"photo_path": _list_thumbnail()}
    column_formatters_detail = {
        "photo_path": _list_thumbnail(400),
        "creation_date":
            lambda view, context, model, name: model.creation_date.strftime("%d %B %Y %H:%M:%S"),
        "modification_date":
            lambda view, context, model, name: model.modification_date.strftime("%d %B %Y %H:%M:%S")
        if model.modification_date
        else "",
    }
    form_extra_fields = {
        "photo_path": form.ImageUploadField("",
            base_path=os.path.join(file_path, "ahelp", "static", "goals_foundation"),
            url_relative_path="/goals_foundation/",
            namegen=generate_image_name,
            allowed_extensions=["jpg", "png", "jpeg", "gif"],
            max_size=(1200, 780, True),
            thumbnail_size=(100, 100, True),
            validators=[validate_directory],
            description='''<span style="color: #007bff">
                           <b style="font-size: 14px">
                           Виберіть фото для карток з
                           поточнимими напрямками фонду.</b></span>'''
        )
    }
