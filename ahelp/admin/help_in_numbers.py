import os

from flask import url_for, Markup
from flask_admin import form

from ahelp.admin.common import AdminModelView, file_path

BASE_PATH = os.path.join(file_path, "ahelp", "static", "help_in_numbers")
os.makedirs(BASE_PATH, exist_ok=True)


class HelpInNumbersAdminModelView(AdminModelView):
    column_list = [
        "photo_path",
        "photo_path_en",
        "photo_path_adaptive",
        "photo_path_adaptive_en",
        "creation_date",
        "modification_date",
    ]
    column_labels = {
        "photo_path": "Фотографія",
        "photo_path_en": "Фотографія(EN)",
        "photo_path_adaptive": "Фотографія(Мобільна версія)",
        "photo_path_adaptive_en": "Фотографія(Мобільна версія - EN)",
        "creation_date": "Дата створення",
        "modification_date": "Дата змінення",
    }
    form_excluded_columns = (
        "modification_date",
        "creation_date",
    )
    column_descriptions = dict(
        photo_path="Фото для блоку 'наша допомога в цифрах'.",
        photo_path_en="Фото для блоку 'наша допомога в цифрах' англійською.",
        photo_path_adaptive="Мобільна версія фото для блоку 'наша допомога в цифрах'",
        photo_path_adaptive_en="Мобільна версія фото для блоку 'наша допомога в цифрах' англійською.",
    )
    column_exclude_list = [
        "creation_date",
        "modification_date",
    ]

    fields = [
        {
            "name": "photo_path",
            "description": '<span style="color: #007bff"><b style="font-size: 14px">Виберіть фото для блоку "наша допомога в цифрах"</b></span>',
        },
        {
            "name": "photo_path_en",
            "description": '<span style="color: #007bff"><b style="font-size: 14px">Виберіть фото для блоку "наша допомога в цифрах" англійською.</b></span>',
        },
        {
            "name": "photo_path_adaptive",
            "description": '<span style="color: #007bff"><b style="font-size: 14px">Виберіть фото для блоку "наша допомога в цифрах", для мобільної версії.</b></span>',
        },
        {
            "name": "photo_path_adaptive_en",
            "description": '<span style="color: #007bff"><b style="font-size: 14px">Виберіть фото для мобільної версії блоку "наша допомога в цифрах", для мобільної версії англійською.</b></span></b></span>',
        },
    ]

    form_extra_fields = {}
    for field in fields:
        form_extra_fields[field["name"]] = form.FileUploadField("", base_path=BASE_PATH, description=field["description"])
    can_view_details = True
    details_modal = True

    def _list_thumbnail(column_name, width):
        def formatter(view, context, model, name):
            if not getattr(model, column_name):
                return ""
            url = url_for("static", filename=os.path.join("help_in_numbers/", getattr(model, column_name, None)))
            if getattr(model, column_name).split(".")[-1] in ["jpg", "jpeg", "png", "svg", "gif", "PNG"]:
                return Markup(f'<img src={url} width="{width}">')

        return formatter

    column_formatters = {
        "photo_path": _list_thumbnail("photo_path", 100),
        "photo_path_en": _list_thumbnail("photo_path_en", 100),
        "photo_path_adaptive": _list_thumbnail("photo_path_adaptive", 100),
        "photo_path_adaptive_en": _list_thumbnail("photo_path_adaptive_en", 100),
    }
    column_formatters_detail = {
        "photo_path": _list_thumbnail("photo_path", 500),
        "photo_path_en": _list_thumbnail("photo_path_en", 500),
        "photo_path_adaptive": _list_thumbnail("photo_path_adaptive", 500),
        "photo_path_adaptive_en": _list_thumbnail("photo_path_adaptive_en", 500),
        "creation_date": lambda view, context, model, name: model.creation_date.strftime("%d %B %Y %H:%M:%S"),
        "modification_date": lambda view, context, model, name: model.modification_date.strftime("%d %B %Y %H:%M:%S")
        if model.modification_date
        else "",
    }
