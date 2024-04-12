import re
from datetime import datetime

from urllib.parse import urlparse

from ahelp.models import ContactsModel
from ahelp.extensions import ma, db
from marshmallow import validate, ValidationError


def validate_html_or_url(value):
    is_html = bool(re.search(r"<.*?>", value))
    is_url = urlparse(value).scheme in ["http", "https"]
    if not is_html and not is_url:
        raise ValidationError("Value should be either HTML or URL")


class ContactsSchema(ma.SQLAlchemyAutoSchema):
    id: int = ma.Int(dump_only=True)
    number: str = ma.String(required=True, validate=validate.Length(min=6, max=15))
    email: str = ma.String(required=True, validate=validate.Email())
    address: str = ma.String(required=True, validate=validate.Length(min=10, max=200))
    address_en: str = ma.String(required=True, validate=validate.Length(min=10, max=200))
    facebook: str = ma.String(required=True, validate=validate.Length(min=3, max=100))
    instagram: str = ma.String(required=True, validate=validate.Length(min=3, max=100))
    telegram: str = ma.String(required=True, validate=validate.Length(min=3, max=100))
    viber: str = ma.String(required=True, validate=validate.Length(min=3, max=100))
    photo_path: str = ma.String(required=True, validate=validate.Regexp(r"^.*\.(png|jpg|jpeg|gif|bmp)$", error="Invalid image format"))
    google_maps: str = ma.String(required=True, validate=validate_html_or_url)
    creation_date: datetime = ma.DateTime(dump_only=True)
    modification_date: datetime = ma.DateTime(dump_only=True)

    class Meta:
        model = ContactsModel
        sqla_session = db.session
        load_instance = True
