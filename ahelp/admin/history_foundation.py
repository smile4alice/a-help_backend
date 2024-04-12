import uuid
import os

from wtforms import MultipleFileField, TextAreaField
from flask import Markup

from ahelp.admin.common import AdminModelView, file_path


HISTORY_DIR = os.path.join(file_path, "ahelp", "static", "history_foundation")

class HistoryFoundationAdminModelView(AdminModelView):
    column_list = [
        "media_path",
        "title",
        "title_en",
        "description",
        "description_en",
        "creation_date",
        "modification_date",
    ]
    column_labels = {
        "media_path": "Шлях до медіа",
        "title": "Заголовок",
        "title_en": "Заголовок(EN)",
        "description": "Опис",
        "description_en": "Опис(EN)",
        "creation_date": "Дата створення",
        "modification_date": "Дата змінення",
    }
    form_columns = (
        "title",
        "title_en",
        "description",
        "description_en",
        "media_path",
    )
    form_excluded_columns = (
        "modification_date",
        "creation_date",
    )
    column_exclude_list = [
        "creation_date",
        "modification_date",
    ]
    column_editable_list = [
        "title",
        "title_en",
    ]
    column_descriptions = dict(
        media_path="Фотографії для сторінки Історія фонду.",
        description="""Опис для сторінки 'Історія фонду'
                       підтримує виділення тексту html тегами
                       наприклад &lt;b&gt;жирний шрифт&lt;/b&gt;.""",
        description_en="""Опис для сторінки англійською підтримує
                          виділення тексту html тегами 
                          наприклад &lt;b&gt;жирний шрифт&lt;/b&gt;.""",
    )
    can_view_details = True
    details_modal = True

    def convert_files_to_paths(form, field):
        file_paths = []
        if field.data:
            os.makedirs(HISTORY_DIR, exist_ok=True)
            for file in field.data:
                if file:
                    filename = f'{uuid.uuid4().hex[:16]}.{file.filename.split(".")[-1]}'
                    file.save(os.path.join(HISTORY_DIR, filename))
                    file_paths.append(os.path.join("static", "history_foundation", filename))
            field.data = " ".join(file_paths)

    form_extra_fields = {
        "media_path": MultipleFileField("",
                                        validators=[convert_files_to_paths],
                                        description='''<span style="color: #007bff">
                                                    <b style="font-size: 14px">
                                                    Фотографії для сторінки "Історія фонду".
                                                    </b></span>''',
        ),
        "description": TextAreaField("Опис", 
                                     render_kw={
                                                "class": "form-control",
                                                "rows": 4,
                                                "style": "border: 0.5px solid #007bff"
            }
        ),
        "description_en": TextAreaField("Опис (EN)",
                                        render_kw={
                                                   "class": "form-control",
                                                   "rows": 4,
                                                   "style": "border: 0.5px solid #007bff"
            }
        ),
    }

    def _list_thumbnail(size = 60):
        def thumbnail_formatter(view, context, model, name):
            if not model.media_path:
                return ""
            paths = model.media_path.split()
            thumbnails = ""
            for path in paths:
                thumbnails += f'<img src=/{path} width={size}>'
            return Markup(thumbnails)
        return thumbnail_formatter

    column_formatters = {"media_path": _list_thumbnail()}
    column_formatters_detail = {
        "media_path": _list_thumbnail(200),
        "creation_date": 
            lambda view, context, model, name: model.creation_date.strftime("%d %B %Y %H:%M:%S"),
        "modification_date":
            lambda view, context, model, name: model.modification_date.strftime("%d %B %Y %H:%M:%S")
        if model.modification_date
        else "",
    }
