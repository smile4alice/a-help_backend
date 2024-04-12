from flask_restful import Resource, abort
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from flask import current_app

from ahelp.models import HeroModel
from ahelp.api.schemas import HeroSchema


class HeroResource(Resource):
    """Hero block resource

    This resource allows the retrieval of data from the Hero block. The data can be retrieved in either English or the default language.

    ---
    get:
        tags:
            - api
        summary: Get data from blocks of <HERO>
        description: Retrieve data from the Hero block in either English or the default language.
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
                                media_path:
                                    type: array
                                    items:
                                        type: string
                                        description: The Path to media.
                                slogan:
                                    type: string
                                    description: A slogan calling for action.
                                description:
                                    type: string
                                    description: Event card description.
                                call_to_action:
                                    type: string
                                    description: A line with a text calling for action.

            400:
                description: ValueError or KeyError when receiving data from the server
            404:
                description: No data found from bloks hero, needs or success stoties
            500:
                description: ValidationError, AttributeError or Unexpected error when transmitting data from the server
    """

    method_decorators = [jwt_required()]

    def get(self, language=None):
        try:
            hero_data = HeroModel.query.filter(HeroModel.active == True).first_or_404(description=("Hero block data not found"))
            schema_hero = HeroSchema()
            slogan_key = "slogan_en" if language == "en" else "slogan"
            description_key = "description_en" if language == "en" else "description"
            call_to_action_key = "call_to_action_en" if language == "en" else "call_to_action"
            local_hero_data = {
                "id": getattr(hero_data, "id", None),
                "media_path": [
                    f"{current_app.config.get('BASE_URL')}/{link}"
                    for link in getattr(hero_data, "media_path", " ").split(" ")
                    if link
                ],
                "slogan": getattr(hero_data, slogan_key, None),
                "description": getattr(hero_data, description_key, None),
                "call_to_action": getattr(hero_data, call_to_action_key, None),
            }
            return schema_hero.dump(local_hero_data)

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
