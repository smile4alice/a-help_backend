from datetime import datetime

from marshmallow import validate

from ahelp.models import GoalsFoundationModel
from ahelp.extensions import ma, db


class GoalsFoundationSchema(ma.SQLAlchemyAutoSchema):
    id: int = ma.Integer(dump_only=True)
    photo_path: str = ma.String(required=True, validate=validate.Regexp(r"^.*\.(png|jpg|jpeg|gif|bmp)$", error="Invalid image format"))
    title: str = ma.String(required=True, validate=validate.Length(min=3, max=100))
    title_en: str = ma.String(required=True, validate=validate.Length(min=3, max=100))
    description: str = ma.String(required=True, validate=validate.Length(min=10, max=600))
    description_en: str = ma.String(required=True, validate=validate.Length(min=10, max=600))
    creation_date: datetime = ma.DateTime(dump_only=True)
    modification_date: datetime = ma.DateTime(dump_only=True)

    class Meta:
        model = GoalsFoundationModel
        sqla_session = db.session
        load_instance = True
