from datetime import datetime

from marshmallow import validate

from ahelp.models import HeroModel
from ahelp.extensions import ma, db


class HeroSchema(ma.SQLAlchemyAutoSchema):
    id: int = ma.Int(dump_only=True)
    active: str = ma.Bool(required=True, validate=validate.OneOf([True, False]))
    media_path: str = ma.List(
        ma.String(required=True, validate=validate.Regexp(r"^.*\.(png|jpg|jpeg|gif|bmp)$", error="Invalid image format"))
    )
    slogan: str = ma.String(required=True, validate=validate.Length(min=5, max=100))
    slogan_en: str = ma.String(required=True, validate=validate.Length(min=5, max=100))
    description: str = ma.String(required=True, validate=validate.Length(min=10))
    description_en: str = ma.String(required=True, validate=validate.Length(min=10))
    call_to_action: str = ma.String(required=True, validate=validate.Length(min=10, max=600))
    call_to_action_en: str = ma.String(required=True, validate=validate.Length(min=10, max=600))
    creation_date: datetime = ma.DateTime(dump_only=True)
    modification_date: datetime = ma.DateTime(dump_only=True)

    class Meta:
        model = HeroModel
        sqla_session = db.session
        load_instance = True
