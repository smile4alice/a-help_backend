from datetime import datetime

from marshmallow import validate

from ahelp.models import HistoryFoundationModel
from ahelp.extensions import ma, db


class HistoryFoundationSchema(ma.SQLAlchemyAutoSchema):
    id: int = ma.Integer(dump_only=True)
    title: str = ma.String(required=True, validate=validate.Length(min=3, max=100))
    title_en: str = ma.String(required=True, validate=validate.Length(min=3, max=100))
    description: str = ma.String(required=True, validate=validate.Length(min=10))
    description_en: str = ma.String(required=True, validate=validate.Length(min=10))
    media_path: list = ma.List(
        ma.String(required=True, validate=validate.Regexp(r"^.*\.(png|jpg|jpeg|gif|bmp)$", error="Invalid image format"))
    )
    creation_date: datetime = ma.String(dump_only=True)
    modification_date: datetime = ma.String(dump_only=True)

    class Meta:
        model = HistoryFoundationModel
        sqla_session = db.session
        load_instance = True
