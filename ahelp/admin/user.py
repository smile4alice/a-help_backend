from flask import current_app

from ahelp.admin.common import AdminModelView
from ahelp.extensions import pwd_context


class UserAdminModelView(AdminModelView):
    column_list = ["username", "active", "admin", "description", "password"]
    column_exclude_list = "password"
    column_labels = {
        "username": "Логін",
        "password": "Пароль",
        "active": "Aктивований",
        "admin": "Адміністратор",
        "description": "Опис",
    }

    def on_model_change(self, form, model, is_created):
        # If creating a new user, hash password
        salt = current_app.config.get("SECRET_KEY").encode("utf-8")
        if is_created:
            model.password = pwd_context.hash(form.password.data, salt=salt)
        else:
            old_password = form.password.object_data
            # If password has been changed, hash password
            if not old_password == model.password:
                model.password = pwd_context.hash(form.password.data)
