import pytest

from ahelp.api.schemas import (
    ContactsSchema,
    FeedbackSchema,
    OurTeamSchema,
    OurPartnersSchema,
    NeedsSchema,
    PaymentSchema,
    PaymentDetailsSchema,
    HistoryFoundationSchema,
    HeroSchema,
    GoalsFoundationSchema,
    DocsAndReportsSchema,
    HelpInNumbersSchema,
)


@pytest.fixture
def contacts_schema():
    return ContactsSchema()


@pytest.fixture
def feedback_schema():
    return FeedbackSchema()


@pytest.fixture
def our_team_schema():
    return OurTeamSchema()


@pytest.fixture
def our_partners_schema():
    return OurPartnersSchema()


@pytest.fixture
def needs_schema():
    return NeedsSchema()


@pytest.fixture
def payment_schema():
    return PaymentSchema()


@pytest.fixture
def history_foundation_schema():
    return HistoryFoundationSchema()


@pytest.fixture
def hero_schema():
    return HeroSchema()


@pytest.fixture
def goals_foundation():
    return GoalsFoundationSchema()


@pytest.fixture
def payment_details_schema():
    return PaymentDetailsSchema()


@pytest.fixture
def docs_and_reports_schema():
    return DocsAndReportsSchema()


@pytest.fixture
def help_in_numbers_schema():
    return HelpInNumbersSchema()
