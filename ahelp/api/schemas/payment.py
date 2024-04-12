from datetime import datetime

from marshmallow import validate

from ahelp.models import PaymentModel
from ahelp.extensions import ma, db


class PaymentSchema(ma.SQLAlchemyAutoSchema):
    id: int = ma.Integer(dump_only=True)
    header: str = ma.String(required=True, validate=validate.Length(min=3, max=100))
    header_en: str = ma.String(required=True, validate=validate.Length(min=3, max=100))
    body: str = ma.String(required=True, validate=validate.Length(min=20, max=600))
    body_en: str = ma.String(required=True, validate=validate.Length(min=20, max=600))
    photo_path: str = ma.String(required=True, validate=validate.Regexp(r"^.*\.(png|jpg|jpeg|gif|bmp)$", error="Invalid image format"))
    title: str = ma.String(required=True, validate=validate.Length(min=3, max=100))
    title_en: str = ma.String(required=True, validate=validate.Length(min=3, max=100))
    description: str = ma.String(required=True, validate=validate.Length(min=20, max=600))
    description_en: str = ma.String(required=True, validate=validate.Length(min=20, max=600))
    creation_date: datetime = ma.DateTime(dump_only=True)
    modification_date: datetime = ma.DateTime(dump_only=True)

    class Meta:
        model = PaymentModel
        sqla_session = db.session
        load_instance = True
