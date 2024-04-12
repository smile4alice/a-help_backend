from datetime import datetime

from sqlalchemy import func
from marshmallow import validate

from ahelp.extensions import db
from ahelp.models import HelpInNumbersModel
from ahelp.extensions import ma, db

allowed_formats = validate.Regexp(r"^.*\.(png|jpg|jpeg|gif|bmp)$", error="Invalid image format")


class HelpInNumbersSchema(ma.SQLAlchemyAutoSchema):
    id: int = ma.Integer(dump_only=True)
    photo_path: str = ma.String(required=True, validate=allowed_formats)
    photo_path_en: str = ma.String(required=True, validate=allowed_formats)
    photo_path_adaptive: str = ma.String(required=True, validate=allowed_formats)
    photo_path_adaptive_en: str = ma.String(required=True, validate=allowed_formats)
    creation_date: datetime = ma.DateTime(dump_only=True)
    modification_date: datetime = ma.DateTime(dump_only=True)

    class Meta:
        model = HelpInNumbersModel
        sqla_session = db.session
        load_instance = True
