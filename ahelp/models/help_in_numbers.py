from datetime import datetime

from sqlalchemy import func

from ahelp.extensions import db


class HelpInNumbersModel(db.Model):
    """Basic model of data for the our help in numbers block"""

    __tablename__ = "Help in numbers"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    photo_path: str = db.Column(db.String)
    photo_path_en: str = db.Column(db.String)
    photo_path_adaptive: str = db.Column(db.String)
    photo_path_adaptive_en: str = db.Column(db.String)
    creation_date: datetime = db.Column(db.DateTime(timezone=True), server_default=func.now())
    modification_date: datetime = db.Column(db.DateTime(timezone=True), onupdate=func.now())
