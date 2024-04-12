from flask_restful import Resource, abort
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from flask import current_app, request

from ahelp.models import NeedsModel
from ahelp.api.schemas import NeedsSchema


class SuccessStoriesResource(Resource):
    """Succes stories resource

    ---
    get:
        tags:
            - api
        summary: Get data from blocks of success stories
        description: Get data from the success stories block, with the possibility to choose a specific language
        parameters:
            - in: path
              name: language
              schema:
                type: string
              description: The language in which the information should be returned. Possible values :\ 'en' for English, 'uk' for Ukrainian. If not provided, the default language will be used.
              default: empty
              example: en
            - in: query
              name: limit
              schema:
                type: integer
              description: Number of items returned from the server.
              default: 0
              example: 4
        responses:
            200:
                content:
                    application/json:
                        schema:
                            type: array
                            items:
                                type: object
                                properties:
                                    id:
                                        type: integer
                                        description: specific story id
                                    media_path:
                                        type: array
                                        items:
                                            type: string
                                            description: The Path to media.
                                    total_amount:
                                        type: integer
                                        description: Amount of money to raise.
                                    title:
                                        type: string
                                        description: Article Title.
                                    description:
                                        type: string
                                        description: Event card description.
            400:
                description: ValueError or KeyError or TypeError when receiving data from the server
            404:
                description: No needs found
            500:
                description: ValidationError, AttributeError or Unexpected error when transmitting data from the server
    """

    method_decorators = [jwt_required()]

    def get(self, language=None):
        try:
            limit = request.args.get("limit") or 0
            if int(limit) > 0:
                needs_data = NeedsModel.query.filter(NeedsModel.active == False).order_by(NeedsModel.creation_date.asc()).limit(limit).all()
            else:
                needs_data = NeedsModel.query.filter(NeedsModel.active == False).order_by(NeedsModel.creation_date.asc()).all()
            if not needs_data:
                abort(404, error="No needs data found")
            schema_needs = NeedsSchema(many=True)
            title_key = "title_en" if language == "en" else "title"
            description_key = "description_en" if language == "en" else "description"
            return schema_needs.dump(
                [
                    {
                        "id": getattr(fild, "id", None),
                        "media_path": [
                            f"{current_app.config.get('BASE_URL')}/{link}"
                            for link in getattr(fild, "media_path", " ").split(" ")
                            if link
                        ],
                        "total_amount": getattr(fild, "total_amount", None),
                        "title": getattr(fild, title_key, None),
                        "description": getattr(fild, description_key, None),
                    }
                    for fild in needs_data
                ],
                many=True,
            )
        except ValidationError as e:
            abort(500, error=f"ValidationError: {str(e)}")
        except AttributeError as e:
            abort(500, error=f"AttributeError: {str(e)}")
        except ValueError as e:
            abort(400, error=f"ValueError: {str(e)}")
        except TypeError as e:
            abort(400, error=f"TypeError: {str(e)}")
        except KeyError as e:
            abort(400, error=f"KeyError: {str(e)}")
        except Exception as e:
            abort(500, error=f"Unexpected error: {str(e)}")
