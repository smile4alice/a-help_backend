from flask_restful import Resource, abort
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from flask import current_app

from ahelp.models import OurTeamModel, OurPartnersModel
from ahelp.api.schemas import OurTeamSchema, OurPartnersSchema


class TeamAndPartnersResource(Resource):
    """
    Team and Partners Information

    ---
    get:
        tags:
            - api
        summary: Get information about our team and partners
        description: Returns information about our team and partners in the specified language or the default language if language is not provided.
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
                description: Information about our team and partners
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                our_team:
                                    type: object
                                    properties:
                                        founder:
                                            type: object
                                            properties:
                                                id:
                                                    type: integer
                                                    example: 1
                                                photo_path:
                                                    type: string
                                                    example: http://site/photos/team_member.jpg
                                                name:
                                                    type: string
                                                    example: Johny Depp
                                                description:
                                                    type: string
                                                    example: Junior
                                        team:
                                            type: object
                                            properties:
                                                id:
                                                    type: integer
                                                    example: 1
                                                photo_path:
                                                    type: string
                                                    example: http://site/photos/team_member.jpg
                                                name:
                                                    type: string
                                                    example: Johny Depp
                                                description:
                                                    type: string
                                                    example: Junior
                                our_partners:
                                    type: array
                                    items:
                                        type: object
                                        properties:
                                            id:
                                                type: integer
                                                example: 1
                                            photo_path:
                                                type: string
                                                example: http://site/photos/partner_logo.png
                                            name:
                                                type: string
                                                example: Example Company
                                            description:
                                                type: string
                                                example: Provider of high-quality products and services
            400:
                description: ValueError or KeyError when receiving data from the server
            404:
                description: No data our team or our partners was found
            500:
                description: ValidationError, AttributeError or Unexpected error when transmitting data from the server
    """

    method_decorators = [jwt_required()]

    def get(self, language=None):
        base_path = f"{current_app.config.get('BASE_URL')}/static"
        try:
            our_team_list = OurTeamModel.query.order_by(OurTeamModel.founder.desc()).all()
            our_partners_list = OurPartnersModel.query.all()
            if not our_team_list or not our_partners_list:
                abort(404, error=f"No data our team or our partners was found")
            our_team_schema = OurTeamSchema()
            our_partners_schema = OurPartnersSchema()
            team_name = "name_en" if language == "en" else "name"
            partner_name = "name_en" if language == "en" else "name"
            team_descr = "description_en" if language == "en" else "description"
            partner_descr = "description_en" if language == "en" else "description"
            local_team = [
                {
                    "id": getattr(fild, "id", None),
                    "photo_path": f"{base_path}/our_team/{getattr(fild, 'photo_path', None)}",
                    "name": getattr(fild, team_name, None),
                    "description": getattr(fild, team_descr, None),
                }
                for fild in our_team_list
            ]
            local_partners = [
                {
                    "id": getattr(fild, "id", None),
                    "photo_path": f"{base_path}/our_partners/{getattr(fild, 'photo_path', None)}",
                    "name": getattr(fild, partner_name, None),
                    "description": getattr(fild, partner_descr, None),
                }
                for fild in our_partners_list
            ]

            return {
                "our_team": {"founder": local_team.pop(0), "team": our_team_schema.dump(local_team, many=True)},
                "our_partners": our_partners_schema.dump(local_partners, many=True),
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
