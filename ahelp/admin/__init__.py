from ahelp.admin.common import (
    AdminModelView,
    CustomAdminIndexView,
    configure_login,
)
from ahelp.admin.user import UserAdminModelView
from ahelp.admin.hero import HeroAdminModelView
from ahelp.admin.needs import NeedsAdminModelView
from ahelp.admin.contacts import ContactsAdminModelView
from ahelp.admin.our_team import OurTeamAdminModelView
from ahelp.admin.our_partners import OurPartnersAdminModelView
from ahelp.admin.payment_details import PaymentDetailsAdminModelView
from ahelp.admin.feedback import FeedbackAdminModelView
from ahelp.admin.payment import PaymentAdminModelView
from ahelp.admin.counter import CounterAdminModelView
from ahelp.admin.docs_and_reports import DocsAndReportsAdminModelView
from ahelp.admin.goals_fondation import GoalsFoundationAdminModelView
from ahelp.admin.history_foundation import HistoryFoundationAdminModelView
from ahelp.admin.help_in_numbers import HelpInNumbersAdminModelView
from ahelp.admin.custom_file_admin import CustomFileAdmin

__all__ = [
    "AdminModelView",
    "CustomAdminIndexView",
    "configure_login",
    "UserAdminModelView",
    "HeroAdminModelView",
    "NeedsAdminModelView",
    "ContactsAdminModelView",
    "OurTeamAdminModelView",
    "OurPartnersAdminModelView",
    "PaymentDetailsAdminModelView",
    "FeedbackAdminModelView",
    "PaymentAdminModelView",
    "CounterAdminModelView",
    "DocsAndReportsAdminModelView",
    "GoalsFoundationAdminModelView",
    "HistoryFoundationAdminModelView",
    "HelpInNumbersAdminModelView",
    "CustomFileAdmin",
]
