from datetime import datetime

from sqlalchemy import func

from ahelp.extensions import db


class OurPartnersModel(db.Model):
    """Basic model of data for foundation partners block"""

    __tablename__ = "Foundation partners"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    photo_path: str = db.Column(db.String)
    name: str = db.Column(db.String(100))
    name_en: str = db.Column(db.String(100))
    description: str = db.Column(db.String(600))
    description_en: str = db.Column(db.String(600))
    creation_date: datetime = db.Column(db.DateTime(timezone=True), server_default=func.now())
    modification_date: datetime = db.Column(db.DateTime(timezone=True), onupdate=func.now())
