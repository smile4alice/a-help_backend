import uuid
import os

from wtforms import MultipleFileField, TextAreaField
from flask import Markup

from ahelp.admin.common import AdminModelView, file_path
from ahelp.models import HeroModel

hero_dir = os.path.join(file_path, "ahelp","static","hero")


class HeroAdminModelView(AdminModelView):
    column_list = [
        "active",
        "media_path",
        "slogan",
        "slogan_en",
        "description",
        "description_en",
        "call_to_action",
        "call_to_action_en",
        "creation_date",
        "modification_date",
    ]
    column_labels = {
        "active": "Статус",
        "media_path": "___Фотографії___",
        "slogan": "Гасло",
        "slogan_en": "Гасло(EN)",
        "description": "Опис",
        "description_en": "Опис(EN)",
        "call_to_action": "Заклик до дії",
        "call_to_action_en": "Заклик до дії(EN)",
        "creation_date": "Дата створення",
        "modification_date": "Дата змінення",
    }
    form_excluded_columns = (
        "modification_date",
        "creation_date",
    )
    column_descriptions = dict(
        active='На сторінці "Заклик до допомоги" відображатиметься тільки активований запис.',
        slogan="Гасло заклику до допомоги.",
        slogan_en="Гасло Англійською.",
        description="Опис потреби, на яку збиратимуться кошти, або успішної історії, в випадку якщо вона не активна.",
        description_en="Опис потреби Англійською, для іноземних відвідувачів сайту.",
        call_to_action="Заклик до допомоги Українською",
        call_to_action_en="Заклик до допомоги, який відображатиметься для іноземних відвідувачів сайту.",
    )
    form_columns = (
        "active",
        "slogan",
        "slogan_en",
        "description",
        "description_en",
        "call_to_action",
        "call_to_action_en",
        "media_path",
    )
    column_searchable_list = [
        "slogan",
        "slogan_en",
        "call_to_action",
        "call_to_action_en",
    ]
    column_exclude_list = [
        "id",
        "creation_date",
        "modification_date",
    ]
    column_editable_list = [
        "active",
        "slogan",
        "slogan_en",
    ]
    text_fields = [
        "description",
        "description_en",
        "call_to_action",
        "call_to_action_en",
    ]
    can_set_page_size = True
    can_view_details = True
    details_modal = True

    def convert_files_to_paths(form, field):
        file_paths = []
        object_data = ''
        if field.data:
            os.makedirs(hero_dir, exist_ok=True)
            if getattr(field, 'object_data', None):
                object_data += field.object_data
            for file in field.data:
                if not getattr(file, 'filename', None) and field.object_data:
                    field.data = field.object_data
                    break
                filename = f'{uuid.uuid4().hex[:16]}.{file.filename.split(".")[-1]}'
                file.save(os.path.join(hero_dir, filename))
                file_paths.append(f"static/hero/{filename}")
        if file_paths:
            hero_all_media = ' '.join([i.media_path for i in HeroModel.query.all()])
            files_in_folder = os.listdir(hero_dir)
            spisok = ' '.join(file_paths) + ' ' + hero_all_media
            for filename in files_in_folder:
                if filename not in spisok or filename in object_data:
                    os.remove(os.path.join(hero_dir, filename))
            field.data = " ".join(file_paths)
    form_extra_fields = {}
    for field_name in text_fields:
        form_extra_fields[field_name] = TextAreaField(
            render_kw={"class": "form-control", "rows": 3, "style": "border: 0.5px solid #007bff"},
        )
    form_extra_fields["media_path"] = MultipleFileField(
        "",
        render_kw={"multiple": True},
        validators=[convert_files_to_paths],
        description='<span style="color: #007bff"><b style="font-size: 14px">Виберіть фото для сторінки із закликом до дії</b></span>',
    )

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
