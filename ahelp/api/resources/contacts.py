from re import findall as re_findall

from flask_restful import Resource, abort, current_app
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required

from ahelp.models import ContactsModel
from ahelp.api.schemas import ContactsSchema


class ContactsResource(Resource):
    """Contacts resource

    ---
    get:
      tags:
        - api
      summary: Get contact information
      description: Get the contact information for the organization
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
          description: Contact information retrieved successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  number:
                    type: string
                    description: The phone number of the organization
                  email:
                    type: string
                    format: email
                    description: The email address of the organization
                  address:
                    type: string
                    description: The address of the organization in the requested language
                  facebook:
                    type: string
                    description: The Facebook page of the organization
                  instagram:
                    type: string
                    description: The Instagram page of the organization
                  telegram:
                    type: string
                    description: The Telegram channel of the organization
                  viber:
                    type: string
                    description: The Viber channel of the organization
                  coordinates:
                    type: string
                    description: The coordinates of the organization
                  photo_path:
                    type: string
                    description: The path to photo.
        404:
            description: No contacts data was found
    """

    method_decorators = [jwt_required()]

    def get(self, language=None):
        try:
            contacts_data = ContactsModel.query.first_or_404(description="No contacts data was found")
            schema_needs = ContactsSchema()
            address_key = "address_en" if language == "en" else "address"
            google_maps = getattr(contacts_data, "google_maps", None)
            local_contacts = {
                "id": getattr(contacts_data, "id", None),
                "number": getattr(contacts_data, "number", None),
                "email": getattr(contacts_data, "email", None),
                "address": getattr(contacts_data, address_key, None),
                "facebook": getattr(contacts_data, "facebook", None),
                "instagram": getattr(contacts_data, "instagram", None),
                "telegram": getattr(contacts_data, "telegram", None),
                "viber": getattr(contacts_data, "viber", None),
                "photo_path": f"{current_app.config.get('BASE_URL')}/static/contacts/{getattr(contacts_data, 'photo_path', None)}",
                "google_maps": re_findall("""(?<=src=['"])(.+)(?=['"]\s?width)""", google_maps)[0] if google_maps else "",
            }
            return schema_needs.dump(local_contacts)
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
