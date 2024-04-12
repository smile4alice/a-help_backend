from datetime import datetime

from sqlalchemy import func

from ahelp.extensions import db


class ContactsModel(db.Model):
    """Basic model of data for contacts block"""

    __tablename__ = "Contacs"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number: str = db.Column(db.String(15))
    email: str = db.Column(db.String(100))
    address: str = db.Column(db.String(200))
    address_en: str = db.Column(db.String(200))
    facebook: str = db.Column(db.String(100))
    instagram: str = db.Column(db.String(100))
    telegram: str = db.Column(db.String(100))
    viber: str = db.Column(db.String(100))
    google_maps: str = db.Column(db.String)
    photo_path: str = db.Column(db.String, nullable=False)
    creation_date: datetime = db.Column(db.DateTime(timezone=True), server_default=func.now())
    modification_date: datetime = db.Column(db.DateTime(timezone=True), onupdate=func.now())
