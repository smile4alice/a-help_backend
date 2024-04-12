from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError

from ahelp.extensions import apispec
from ahelp.api.resources import (
    UserResource,
    UserList,
    HeroResource,
    NeedsResource,
    SuccessStoriesResource,
    FeedbackResource,
    ContactsResource,
    TeamAndPartnersResource,
    CounterResource,
    PaymentResource,
    SuccessFondyResource,
    SuccessPayPalResource,
    DocsAndReportsResource,
    GoalsAndHistoryResource,
    PrivacyPolicyResource,
    FakerResource,
    HelpInNumbersResource,
)
from ahelp.api.schemas import (
    UserSchema,
    HeroSchema,
    NeedsSchema,
    FeedbackSchema,
    PaymentDetailsSchema,
    PaymentSchema,
    ContactsSchema,
    OurTeamSchema,
    OurPartnersSchema,
    DocsAndReportsSchema,
    GoalsFoundationSchema,
    HelpInNumbersSchema,
    # CounterSchema,
)


blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)


api.add_resource(UserResource, "/users/<int:user_id>", endpoint="user_by_id")
api.add_resource(UserList, "/users", endpoint="users")
api.add_resource(HeroResource, "/hero", "/<string:language>/hero", endpoint="hero")
api.add_resource(NeedsResource, "/needs/", "/<string:language>/needs/", endpoint="needs")
api.add_resource(
    SuccessStoriesResource,
    "/success_stories/",
    "/<string:language>/success_stories/",
    endpoint="success_stories",
)
api.add_resource(FeedbackResource, "/handlers/send_mail")
api.add_resource(ContactsResource, "/contacts/", "/<string:language>/contacts/", endpoint="contacts")
api.add_resource(CounterResource, "/counter/", "/<string:language>/counter/", endpoint="counter")
api.add_resource(
    TeamAndPartnersResource,
    "/team_and_partners/",
    "/<string:language>/team_and_partners/",
    endpoint="team_and_partners",
)
api.add_resource(PaymentResource, "/payment", "/<string:language>/payment", endpoint="payment")
api.add_resource(DocsAndReportsResource, "/docs_and_reports", endpoint="docs_and_reports")
api.add_resource(GoalsAndHistoryResource, "/goals_and_history/", "/<string:language>/goals_and_history/", endpoint="goals_and_history")
api.add_resource(SuccessPayPalResource, "/handlers/payment/paypal/execute")
api.add_resource(SuccessFondyResource, "/handlers/payment/fondy/execute")
api.add_resource(PrivacyPolicyResource, "/privacy_policy", "/<string:language>/privacy_policy", endpoint="privacy_policy")
api.add_resource(HelpInNumbersResource, "/help_in_numbers", "/<string:language>/help_in_numbers", endpoint="help_in_numbers")
api.add_resource(FakerResource, "/handlers/faker")


@blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("UserSchema", schema=UserSchema)
    apispec.spec.components.schema("HeroSchema", schema=HeroSchema)
    apispec.spec.components.schema("NeedsSchema", schema=NeedsSchema)
    apispec.spec.components.schema("FeedbackSchema", schema=FeedbackSchema)
    apispec.spec.components.schema("ContactsSchema", schema=ContactsSchema)
    apispec.spec.components.schema("OurPartnersSchema", schema=OurPartnersSchema)
    apispec.spec.components.schema("OurTeamSchema", schema=OurTeamSchema)
    apispec.spec.components.schema("PaymentDetailsSchema", schema=PaymentDetailsSchema)
    apispec.spec.components.schema("PaymentSchema", schema=PaymentSchema)
    apispec.spec.components.schema("DocsAndReportsSchema", schema=DocsAndReportsSchema)
    apispec.spec.components.schema("GoalsFoundationSchema", schema=GoalsFoundationSchema)
    apispec.spec.components.schema("HelpInNumbersSchema", schema=HelpInNumbersSchema)
    # apispec.spec.components.schema("CounterSchema", schema=CounterSchema)
    apispec.spec.path(view=UserResource, app=current_app)
    apispec.spec.path(view=UserList, app=current_app)
    apispec.spec.path(view=HeroResource, app=current_app)
    apispec.spec.path(view=NeedsResource, app=current_app)
    apispec.spec.path(view=SuccessStoriesResource, app=current_app)
    apispec.spec.path(view=FeedbackResource, app=current_app)
    apispec.spec.path(view=ContactsResource, app=current_app)
    apispec.spec.path(view=TeamAndPartnersResource, app=current_app)
    apispec.spec.path(view=PaymentResource, app=current_app)
    apispec.spec.path(view=DocsAndReportsResource, app=current_app)
    apispec.spec.path(view=GoalsAndHistoryResource, app=current_app)
    apispec.spec.path(view=PrivacyPolicyResource, app=current_app)
    apispec.spec.path(view=HelpInNumbersResource, app=current_app)
    # apispec.spec.path(view=CounterResource, app=current_app)


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400
