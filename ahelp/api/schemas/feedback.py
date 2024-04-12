from datetime import datetime

from marshmallow import validate

from ahelp.models import FeedbackModel
from ahelp.extensions import ma, db


class FeedbackSchema(ma.SQLAlchemyAutoSchema):
    id: int = ma.Integer(dump_only=True)
    name: str = ma.String(required=True, validate=validate.Length(min=3, max=100))
    number: str = ma.String(required=False, validate=validate.Length(min=6, max=15))
    mail: str = ma.String(required=True, validate=validate.Email())
    message: str = ma.String(required=True, validate=validate.Length(min=1, max=1000))
    date: datetime = ma.DateTime(dump_only=True)

    class Meta:
        model = FeedbackModel
        sqla_session = db.session
        load_instance = True
