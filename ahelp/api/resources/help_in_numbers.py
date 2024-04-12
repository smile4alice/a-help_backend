from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask import abort, current_app
from marshmallow import ValidationError

from ahelp.models import HelpInNumbersModel


class HelpInNumbersResource(Resource):
    """To represent the help in numbers block
    ---
    get:
        tags:
            - api
        summary: Get data from help in numbers block
        description: Get data fromhelp in numbers block, with the possibility to choose a specific language
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
                                    description: specific help in numbers id
                                photo_path:
                                    type: string
                                    description: The photo_path for help in numbers block
                                photo_path_adaptive:
                                    type: string
                                    descriptions: The photo_path for adaptive version for help in numbers block
            400:
                description: ValueError or KeyError when receiving data from the server
            404:
                description: No help in numbers data found
            500:
                description: ValidationError, AttributeError or Unexpected error when transmitting data from the server
    """

    method_decorators = [jwt_required()]

    def get(self, language=None):
        base_path = f"{current_app.config.get('BASE_URL')}/static/help_in_numbers/"
        help_in_numbers_data = HelpInNumbersModel.query.order_by(HelpInNumbersModel.creation_date.asc()).first_or_404(
            description="Help in numbers block data not found"
        )
        try:
            photo_path = "photo_path_en" if language == "en" else "photo_path"
            photo_path_adaptive = "photo_path_adaptive_en" if language == "en" else "photo_path_adaptive"
            return {
                "id": getattr(help_in_numbers_data, "id", None),
                "photo_path": f"{base_path}{getattr(help_in_numbers_data, photo_path, None)}",
                "photo_path_adaptive": f"{base_path}{getattr(help_in_numbers_data, photo_path_adaptive, None)}",
            }
        except ValueError as e:
            abort(400, error=f"ValueError: {str(e)}")
        except ValidationError as e:
            abort(400, error=f"ValidationError: {str(e)}")
        except KeyError as e:
            abort(400, error=f"KeyError: {str(e)}")
        except AttributeError as e:
            abort(500, error=f"AttributeError: {str(e)}")
        except Exception as e:
            abort(500, error=f"Unexpected error: {str(e)}")
