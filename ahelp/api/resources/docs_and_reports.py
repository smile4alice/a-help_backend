from flask_restful import Resource, abort
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required
from flask import current_app

from ahelp.models import DocsAndReportsModel
from ahelp.api.schemas import DocsAndReportsSchema


class DocsAndReportsResource(Resource):
    """To represent the docs and reports of the foundation
    ---
    get:
        tags:
            - api
        summary: Get data from blocks of docs and reports
        description: Get data from blocks of docs and reports, with the possibility to choose a specific language
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
                                    description: specific goals id
                                statutes:
                                    type: string
                                    description: Path to the file with information about the statutes of the charity
                                ownership_structure:
                                    type: string
                                    description: Path to the file with information about the ownership structure of the charity
                                photo_path:
                                    type: string
                                    description: Path to a photo with a certificate or award from a charitable organization
                                bank_account_holder_certificate:
                                    type: string
                                    description: Path to the file with information about the bank account holder certificate of the charity
                                certificate_of_nonprofit_organization:
                                    type: string
                                    description: Path to the file with information about the cerificate of nonprofit organization of the charity
                                extract_from_unified_state_register:
                                    type: string
                                    description: Path to the file with information about the extract from inified state register of the charity
                                annual_report:
                                    type: string
                                    description: Path to the file with information about the annual report of the charity
            400:
                description: ValueError or KeyError when receiving data from the server
            404:
                description: No docs or reports found
            500:
                description: ValidationError, AttributeError or Unexpected error when transmitting data from the server
    """

    method_decorators = [jwt_required()]

    def get(self):
        base_path = f"{current_app.config.get('BASE_URL')}/static/docs_and_reports/"
        try:
            docs_and_reports_data = DocsAndReportsModel.query.first_or_404(description="Docs and reports block data not found")
            schema_docs_and_reports = DocsAndReportsSchema()
            return schema_docs_and_reports.dump(
                {
                    "id": getattr(docs_and_reports_data, "id", None),
                    "statutes": f"{base_path}{getattr(docs_and_reports_data, 'statutes', None)}",
                    "ownership_structure": f"{base_path}{getattr(docs_and_reports_data, 'ownership_structure', None)}",
                    "photo_path": f"{base_path}{getattr(docs_and_reports_data, 'photo_path', None)}",
                    "bank_account_holder_certificate": f"{base_path}{getattr(docs_and_reports_data, 'bank_account_holder_certificate', None)}",
                    "certificate_of_nonprofit_organization": f"{base_path}{getattr(docs_and_reports_data, 'certificate_of_nonprofit_organization', None)}",
                    "extract_from_unified_state_register": f"{base_path}{getattr(docs_and_reports_data, 'extract_from_unified_state_register', None)}",
                    "annual_report": f"{base_path}{getattr(docs_and_reports_data, 'annual_report', None)}",
                }
            )
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
