from datetime import datetime

from marshmallow import validate

from ahelp.models import NeedsModel
from ahelp.extensions import ma, db


class NeedsSchema(ma.SQLAlchemyAutoSchema):
    id: int = ma.Integer(dump_only=True)
    active: bool = ma.Boolean(required=True, validate=validate.OneOf([True, False]))
    media_path: list = ma.List(
        ma.String(required=True, validate=validate.Regexp(r"^.*\.(png|jpg|jpeg|gif|bmp)$", error="Invalid image format"))
    )
    title: str = ma.String(required=True, validate=validate.Length(min=3, max=100))
    title_en: str = ma.String(required=True, validate=validate.Length(min=3, max=100))
    total_amount: str = ma.Integer(required=True, validate=validate.Range(min=1))
    description: str = ma.String(required=True, validate=validate.Length(min=10))
    description_en: str = ma.String(required=True, validate=validate.Length(min=10))
    creation_date: datetime = ma.String(dump_only=True)
    modification_date: datetime = ma.String(dump_only=True)

    class Meta:
        model = NeedsModel
        sqla_session = db.session
        load_instance = True
