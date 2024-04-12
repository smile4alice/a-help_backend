import uuid
import os

from wtforms import MultipleFileField, TextAreaField
from flask import Markup

from ahelp.admin.common import AdminModelView, file_path
from ahelp.models import NeedsModel

needs_dir = os.path.join(file_path, "ahelp", "static", "needs")


class NeedsAdminModelView(AdminModelView):
    column_list = [
        "active",
        "media_path",
        "title",
        "title_en",
        "total_amount",
        "description",
        "description_en",
        "creation_date",
        "modification_date",
    ]
    column_labels = {
        "active": "Статус",
        "media_path": "___Фотографії___",
        "title": "Заголовок",
        "title_en": "Заголовок(EN)",
        "total_amount": "Сума",
        "description": "Опис",
        "description_en": "Опис(EN)",
        "creation_date": "Дата створення",
        "modification_date": "Дата змінення",
    }
    column_searchable_list = [
        "title",
        "title_en",
    ]
    column_exclude_list = [
        "creation_date",
        "modification_date",
    ]
    column_editable_list = [
        "total_amount",
        "active",
    ]
    form_excluded_columns = (
        "modification_date",
        "creation_date",
    )
    form_columns = (
        "active",
        "title",
        "title_en",
        "total_amount",
        "description",
        "description_en",
        "media_path",
    )
    column_descriptions = dict(
        active='''Якщо історія активна, вона відображатиметься в блоці "Поточні потреби",
                  якщо не активна - в блоці "Успішні історії".''',
        title="заголовок поточної потреби або успішної історії, якщо не активна.",
        title_en="Заголовок поточної потреби або успішної історії англійською.",
        total_amount="Загальна сума коштів, яку потрібно зібрати",
        description="""Опис потреби, на яку збиратимуться кошти,
                       або успішної історії, в випадку якщо вона не активна.""",
        description_en="Опис потреби англійською, для іноземних відвідувачів сайту.",
    )
    form_excluded_columns = "modification_date"
    can_set_page_size = True
    can_view_details = True
    details_modal = True
    list_template = "admin/details_button.html"

    def render(self, template, **kwargs):
        kwargs[
            "description"
        ] = """Історії можуть бути активними або не активними.
               В залежності від статусу, вони відображатимуться
               у відповідних розділах сайту. Будьте уважні."""
        return super(NeedsAdminModelView, self).render(template, **kwargs)

    def convert_files_to_paths(form, field):
        file_paths = []
        object_data = ''
        if field.data:
            os.makedirs(needs_dir, exist_ok=True)
            if getattr(field, 'object_data', None):
                object_data += field.object_data
            for file in field.data:
                if not getattr(file, 'filename', None) and field.object_data:
                    field.data = field.object_data
                    break
                filename = f'{uuid.uuid4().hex[:16]}.{file.filename.split(".")[-1]}'
                file.save(os.path.join(needs_dir, filename))
                file_paths.append(f"static/needs/{filename}")
            if file_paths:
                hero_all_media = ' '.join([i.media_path for i in NeedsModel.query.all()])
                files_in_folder = os.listdir(needs_dir)
                spisok = ' '.join(file_paths) + ' ' + hero_all_media
                for filename in files_in_folder:
                    if filename not in spisok or filename in object_data:
                        os.remove(os.path.join(needs_dir, filename))
                field.data = " ".join(file_paths)

    form_extra_fields = {
        "media_path": 
            MultipleFileField("",
                              render_kw={"multiple": True},
                              validators=[convert_files_to_paths],
                              description='''<span style="color: #007bff">
                                             <b style="font-size: 14px">
                                             Виберіть фото для сторінки "Потреби" 
                                             або "Успішні історії"
                                             (залежно від статусу).</b></span>''',
        ),
        "description": 
            TextAreaField("Опис",
                          render_kw={
                                    "class": "form-control",
                                    "rows": 3,
                                    "style": "border: 0.5px solid #007bff"}
        ),
        "description_en":
            TextAreaField("Опис англійською", 
                          render_kw={
                                    "class": "form-control",
                                    "rows": 3,
                                    "style": "border: 0.5px solid #007bff"}
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

    column_formatters = {"media_path": _list_thumbnail(),}
    column_formatters_detail = {
        "media_path": _list_thumbnail(200),
        "creation_date": 
            lambda view, context, model, name: model.creation_date.strftime("%d %B %Y %H:%M:%S"),
        "modification_date":
            lambda view, context, model, name: model.modification_date.strftime("%d %B %Y %H:%M:%S")
        if model.modification_date
        else "",
    }
