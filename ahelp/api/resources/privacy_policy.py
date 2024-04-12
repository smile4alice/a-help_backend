from flask_restful import Resource, abort, current_app
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from ahelp.models import DocsAndReportsModel


class PrivacyPolicyResource(Resource):
    """Needs resource

    ---
    get:
        tags:
            - api
        summary: Get data from blocks of privacy policy
        description: Get data from the privacy policy blocks, with the possibility to choose a specific language
        parameters:
            - in: path
              name: language
              schema:
                type: string
              description: The language in which the information should be returned. Possible values :\ 'en' for English, 'uk' for Ukrainian. If not provided, the default language will be used.
              default: empty
              example: en
        responses:
            200:
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                id:
                                    type: integer
                                    description: specific privacy policy id
                                privacy_policy:
                                    type: string
                                    description: Path to the privacy policy file
            400:
                description: ValueError or KeyError when receiving data from the server
            404:
                description: No privacy policy data found
            500:
                description: ValidationError, AttributeError or Unexpected error when transmitting data from the server
    """

    method_decorators = [jwt_required()]

    def get(self, language=None):
        try:
            privacy_policy_data = DocsAndReportsModel.query.first_or_404(description="No privacy policy data was found")
            privacy_policy = "privacy_policy_en" if language == "en" else "privacy_policy"

            return {
                "id": getattr(privacy_policy_data, "id", None),
                "privacy_policy": f"{current_app.config.get('BASE_URL')}/static/docs_and_reports/{getattr(privacy_policy_data, privacy_policy, None)}",
            }
        except ValidationError as e:
            abort(500, error=f"ValidationError: {str(e)}")
        except AttributeError as e:
            abort(500, error=f"AttributeError: {str(e)}")
        except ValueError as e:
            abort(400, error=f"ValueError: {str(e)}")
        except KeyError as e:
            abort(400, error=f"KeyError: {str(e)}")
        except Exception as e:
            abort(500, error=f"Unexpected error: {str(e)}")
