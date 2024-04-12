from datetime import datetime

from marshmallow import ValidationError
from sqlalchemy import func

from ahelp.extensions import db


class OurTeamModel(db.Model):
    """Basic model of data for foundation team block"""

    __tablename__ = "Foundation team"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    founder: bool = db.Column(db.Boolean)
    photo_path: str = db.Column(db.String)
    name: str = db.Column(db.String(100))
    name_en: str = db.Column(db.String(100))
    description: str = db.Column(db.String(600))
    description_en: str = db.Column(db.String(600))
    creation_date: datetime = db.Column(db.DateTime(timezone=True), server_default=func.now())
    modification_date: datetime = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def validate(self):
        if len(self.name) < 3:
            raise ValidationError("Name must be at least 3 characters long")
