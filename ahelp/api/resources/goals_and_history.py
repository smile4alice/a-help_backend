from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask import abort, jsonify, current_app
from marshmallow import ValidationError

from ahelp.models import GoalsFoundationModel, HistoryFoundationModel
from ahelp.api.schemas import HistoryFoundationSchema


class GoalsAndHistoryResource(Resource):
    """To represent the goals and history of the foundation
    ---
    get:
        tags:
            - api
        summary: Get data from blocks of goals and history
        description: Get data from blocks of goals and history, with the possibility to choose a specific language
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
                                block_goals:
                                    type: object
                                    properties:
                                        id:
                                            type: integer
                                            description: specific goals id
                                        title:
                                            type: string
                                            description: the title for current card of goals of charity
                                        description:
                                            type: string
                                            description: the description for current card of goals of charity
                                        photo_paths:
                                            type: string
                                            description: The path to the photo for the current goal and description of the goal
                                block_history:
                                    type: object
                                    properties:
                                        id:
                                            type: integer
                                            description: specific goals id
                                        title:
                                            type: string
                                            description: The title for history of the foundation
                                        description:
                                            type: string
                                            descriptions: The history of the foundation
                                        media_path:
                                            type: array
                                            items:
                                                type: string
                                                description: The path to the photo for the current title and description of the goal
            400:
                description: ValueError or KeyError when receiving data from the server
            404:
                description: No goals or history data found
            500:
                description: ValidationError, AttributeError or Unexpected error when transmitting data from the server
    """

    method_decorators = [jwt_required()]

    def get(self, language=None):
        base_path = f"{current_app.config.get('BASE_URL')}/static"
        try:
            goals_data = GoalsFoundationModel.query.first_or_404(description="Goal foundation block data not found")
            history_data = HistoryFoundationModel.query.order_by(HistoryFoundationModel.creation_date.asc()).all()
            if not history_data:
                abort(404, error="History foundation block data not found")
            history_schema = HistoryFoundationSchema(many=True)

            title = "title_en" if language == "en" else "title"
            description = "description_en" if language == "en" else "description"
            history_title = "title_en" if language == "en" else "title"
            history_description = "description_en" if language == "en" else "description"
            return jsonify(
                {
                    "block_goals": {
                        "id": getattr(goals_data, "id", None),
                        "title": getattr(goals_data, title, None),
                        "description": getattr(goals_data, description, None),
                        "photo_path": f"{base_path}/goals_foundation/{getattr(goals_data, 'photo_path', None)}",
                    },
                    "block_history": history_schema.dump(
                        [
                            {
                                "id": getattr(field, "id", None),
                                "title": getattr(field, history_title, None),
                                "description": getattr(field, history_description, None),
                                "media_path": [
                                    f"{base_path}/history_foundation/{link}"
                                    for link in getattr(field, "media_path", " ").split(" ")
                                    if link
                                ],
                            }
                            for field in history_data
                        ],
                        many=True,
                    ),
                }
            )
        except AttributeError as e:
            abort(500, error=f"AttributeError: {str(e)}")
        except ValueError as e:
            abort(400, error=f"ValueError: {str(e)}")
        except ValidationError as e:
            abort(400, error=f"ValidationError: {str(e)}")
        except KeyError as e:
            abort(400, error=f"KeyError: {str(e)}")
        except Exception as e:
            abort(500, error=f"Unexpected error: {str(e)}")
