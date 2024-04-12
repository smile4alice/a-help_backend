import os
import logging
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, Markup
from flask_admin import Admin
from flask_babelex import Babel
from flask_mail import Mail
from flask_cors import CORS

from ahelp import api, auth, manage
from ahelp.extensions import apispec, db, jwt, migrate
from ahelp.models import (
    User,
    HeroModel,
    NeedsModel,
    FeedbackModel,
    ContactsModel,
    OurTeamModel,
    OurPartnersModel,
    PaymentModel,
    PaymentDetailsModel,
    DocsAndReportsModel,
    GoalsFoundationModel,
    HistoryFoundationModel,
    HelpInNumbersModel,
    # CounterModel,
)
from ahelp.admin import (
    configure_login,
    CustomAdminIndexView,
    CustomFileAdmin,
    UserAdminModelView,
    HeroAdminModelView,
    NeedsAdminModelView,
    ContactsAdminModelView,
    OurTeamAdminModelView,
    OurPartnersAdminModelView,
    OurPartnersAdminModelView,
    PaymentDetailsAdminModelView,
    FeedbackAdminModelView,
    PaymentAdminModelView,
    FeedbackAdminModelView,
    PaymentAdminModelView,
    DocsAndReportsAdminModelView,
    HistoryFoundationAdminModelView,
    GoalsFoundationAdminModelView,
    HelpInNumbersAdminModelView,
    # CounterAdminModelView,
)


def create_app(testing=False):
    """Application factory, used to create application"""
    app = Flask("ahelp")
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.config.from_object("ahelp.config")
    # Object to configure localization
    Babel(app)

    if testing is True:
        app.config["TESTING"] = True

    configure_extensions(app)
    configure_cli(app)
    configure_apispec(app)
    configure_login(app)
    register_blueprints(app)
    register_adminsite(app)
    configure_mails(app)
    app.before_first_request(configure_logger)
    return app


def configure_extensions(app):
    """Configure flask extensions"""
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)


def configure_cli(app):
    """Configure Flask 2.0's cli for easy entity management"""
    app.cli.add_command(manage.init)


def configure_apispec(app):
    """Configure APISpec for swagger support"""
    apispec.init_app(app, security=[{"jwt": []}])
    apispec.spec.components.security_scheme("jwt", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"})
    apispec.spec.components.schema(
        "PaginatedResult",
        {
            "properties": {
                "total": {"type": "integer"},
                "pages": {"type": "integer"},
                "next": {"type": "string"},
                "prev": {"type": "string"},
            }
        },
    )


def register_blueprints(app):
    """Register all blueprints for application"""
    app.register_blueprint(auth.views.blueprint)
    app.register_blueprint(api.views.blueprint)


def configure_mails(app):
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 465
    app.config["MAIL_USE_SSL"] = True
    app.config["MAIL_USERNAME"] = app.config.get("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = app.config.get("MAIL_PASSWORD")
    Mail(app)


def configure_logger():
    os.makedirs(os.path.join(".", "ahelp", "static", "logs"), exist_ok=True)
    logs_file_level = logging.WARNING
    logs_file_format = "%(levelname)-8s | %(asctime)-20s| %(message)s"
    logs_file_date_format = "%H:%M:%S %d-%m-%Y"
    logs_file_path = os.path.join(".", "ahelp", "static", "logs", "log_data.log")
    logs_file_timeout = "D"  # D, M, H, S, W0, W1, midnight
    logs_file_interval = 1
    logs_file_backupcount = 7
    logger = logging.getLogger()
    rotation_file_handler = TimedRotatingFileHandler(
        logs_file_path, when=logs_file_timeout, interval=logs_file_interval, backupCount=logs_file_backupcount
    )
    rotation_file_handler.namer = lambda name: name.replace(".log", "") + ".log"
    rotation_file_handler.setLevel(logs_file_level)
    rotation_file_handler.setFormatter(logging.Formatter(logs_file_format, logs_file_date_format))
    console_hanlder = logging.StreamHandler()
    logger.addHandler(rotation_file_handler)
    logger.addHandler(console_hanlder)


def register_adminsite(app):
    app.config["FLASK_ADMIN_FLUID_LAYOUT"] = True
    base_url = os.getenv("MAIN_PAGE_URL")
    header = f'<a href="{base_url}" title="На домашню сторінку A-Help">\
               <img src="/static/interface/a-help_logo.png" height="40" width="90"></a>'
    admin = Admin(
        app,
        name=Markup(header),
        index_view=CustomAdminIndexView(),
        base_template="master.html",
        template_mode="bootstrap4",
    )

    admin.add_view(UserAdminModelView(User, db.session, name="Користувачі", category="Керування"))
    admin.add_view(FeedbackAdminModelView(FeedbackModel, db.session, name="Feedback logs"))
    admin.add_view(PaymentAdminModelView(PaymentModel, db.session, name="Розділ для донатів", category="Дані блоків"))
    admin.add_view(HelpInNumbersAdminModelView(HelpInNumbersModel, db.session, name="Наша допомога в цифрах", category="Дані блоків"))
    admin.add_view(PaymentDetailsAdminModelView(PaymentDetailsModel, db.session, name="Реквізити", category="Дані блоків"))
    admin.add_view(ContactsAdminModelView(ContactsModel, db.session, name="Контакти", category="Дані блоків"))
    admin.add_view(OurTeamAdminModelView(OurTeamModel, db.session, name="Наша команда", category="Дані блоків"))
    admin.add_view(OurPartnersAdminModelView(OurPartnersModel, db.session, name="Наші партнери", category="Дані блоків"))
    admin.add_view(DocsAndReportsAdminModelView(DocsAndReportsModel, db.session, name="Документи та звіти", category="Дані блоків"))
    admin.add_view(GoalsFoundationAdminModelView(GoalsFoundationModel, db.session, name="Мета фонду", category="Дані блоків"))
    admin.add_view(HistoryFoundationAdminModelView(HistoryFoundationModel, db.session, name="Історія фонду", category="Дані блоків"))
    admin.add_view(HeroAdminModelView(HeroModel, db.session, name="Блок <HERO>"))
    admin.add_view(NeedsAdminModelView(NeedsModel, db.session, name="Блоки <NEEDS> та <SUCCESS STORIES>"))
    # admin.add_view(CounterAdminModelView(CounterModel, db.session, name="Лічильник", category="Статистика"))
    
    path = os.path.join(os.path.dirname(__file__), "static")
    admin.add_view(CustomFileAdmin(path, "/static/", name="Файловий Менеджер", category="Керування"))
