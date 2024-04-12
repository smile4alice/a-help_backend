from datetime import datetime

from sqlalchemy import func

from ahelp.extensions import db


class NeedsModel(db.Model):
    """Basic model of data for current neeeds block"""

    __tablename__ = "Current needs"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    active: bool = db.Column(db.Boolean)
    media_path: str = db.Column(db.String, nullable=False)
    title: str = db.Column(db.String(100), nullable=False)
    title_en: str = db.Column(db.String(100), nullable=False)
    total_amount: str = db.Column(db.Integer, nullable=False)
    description: str = db.Column(db.String, nullable=False)
    description_en: str = db.Column(db.String, nullable=False)
    creation_date: datetime = db.Column(db.DateTime(timezone=True), server_default=func.now())
    modification_date: datetime = db.Column(db.DateTime(timezone=True), onupdate=func.now())
