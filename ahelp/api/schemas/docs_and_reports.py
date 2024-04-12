from datetime import datetime

from marshmallow import validate

from ahelp.models import DocsAndReportsModel
from ahelp.extensions import ma, db

allowed_formats = validate.Regexp(r"^.*\.(png|jpg|jpeg|pdf|bmp|csv|txt|rtf|doc|tiff)$", error="Invalid image format")


class DocsAndReportsSchema(ma.SQLAlchemyAutoSchema):
    id: int = ma.Integer(dump_only=True)
    statutes: str = ma.String(required=False, validate=allowed_formats)
    ownership_structure: str = ma.String(required=False, validate=allowed_formats)
    photo_path: str = ma.String(required=False, validate=allowed_formats)
    bank_account_holder_certificate: str = ma.String(required=False, validate=allowed_formats)
    certificate_of_nonprofit_organization: str = ma.String(required=False, validate=allowed_formats)
    extract_from_unified_state_register: str = ma.String(required=False, validate=allowed_formats)
    annual_report: str = ma.String(required=False, validate=allowed_formats)
    privacy_policy: str = ma.String(required=False, validate=allowed_formats)
    privacy_policy_en: str = ma.String(required=False, validate=allowed_formats)
    creation_date: datetime = ma.DateTime(dump_only=True)
    modification_date: datetime = ma.DateTime(dump_only=True)

    class Meta:
        model = DocsAndReportsModel
        sqla_session = db.session
        load_instance = True
