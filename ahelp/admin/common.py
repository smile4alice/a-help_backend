import os

from wtforms import form, fields, validators
from flask import redirect, url_for, request, current_app
import flask_login as login
from flask_admin import AdminIndexView, helpers, expose
from flask_admin.contrib.sqla import ModelView

from ahelp.extensions import db, pwd_context
from ahelp.models import User

file_path = os.path.abspath(os.path.dirname(__name__))


class AdminModelView(ModelView):
    extra_css = ['/static/styles/berry_blue.css']

    create_modal = True
    edit_modal = True

    def is_accessible(self):
        return login.current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
            # return redirect(url_for("login", next=request.url))
        return redirect('/admin/login')


def configure_login(app):
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)


# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
    login = fields.StringField(label="Логін", validators=[validators.InputRequired()])


class LoginForm(form.Form):
    login = fields.StringField(label="Логін", validators=[validators.InputRequired()])
    password = fields.PasswordField(label="Пароль", validators=[validators.InputRequired()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError("Невірний логін")

        # we're comparing hashes
        salt = current_app.config.get("SECRET_KEY").encode("utf-8")
        if not user.password == pwd_context.hash(self.password.data, salt=salt):
            raise validators.ValidationError("Невірний пароль")

        if not user.admin:
            raise validators.ValidationError("Користувач не адміністратор")

    def get_user(self):
        return db.session.query(User).filter_by(username=self.login.data).first()


class CustomAdminIndexView(AdminIndexView):

    @expose("/", methods=("GET", "POST"))
    def index(self):
        self.style_name = 'Berry blue'
        if not login.current_user.is_authenticated:
            return redirect(url_for(".login_view"))
        
        if request.method == 'POST':
            option = request.form.get('options', None)
            if option == 'berry_blue':
                AdminModelView.extra_css = ['/static/styles/berry_blue.css']
                self.style_name = 'Berry blue'
            if option == 'sea_wave':
                AdminModelView.extra_css = ['/static/styles/sea_wave.css']
                self.style_name = 'Sea wave'
            if option == 'green_mist':
                AdminModelView.extra_css = ['/static/styles/green_mist.css']
                self.style_name = 'Green mist'
            if option == 'after_the_rain':
                AdminModelView.extra_css = ['/static/styles/after_the_rain.css']
                self.style_name = 'The forest after the rain'
            if option == 'desert':
                AdminModelView.extra_css = ['/static/styles/desert.css']
                self.style_name = 'The desert'
            if option == 'golden_afternoon':
                AdminModelView.extra_css = ['/static/styles/golden_afternoon.css']
                self.style_name = 'Golden Afternoon'

        self.extra_css = AdminModelView.extra_css
        
        return super(CustomAdminIndexView, self).index()

    @expose("/login/", methods=("GET", "POST"))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for(".index"))

        self._template_args["form"] = form
        return super(CustomAdminIndexView, self).index()

    @expose("/logout/")
    def logout_view(self):
        login.logout_user()
        return redirect(url_for(".index"))
