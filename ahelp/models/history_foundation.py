from datetime import datetime

from sqlalchemy import func

from ahelp.extensions import db


class HistoryFoundationModel(db.Model):
    """Basic model of data for history of the foundation"""

    __tablename__ = "History of the foundation"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title: str = db.Column(db.String(100), nullable=False)
    title_en: str = db.Column(db.String(100), nullable=False)
    description: str = db.Column(db.String, nullable=False)
    description_en: str = db.Column(db.String, nullable=False)
    media_path: str = db.Column(db.String, nullable=False)
    creation_date: datetime = db.Column(db.DateTime(timezone=True), server_default=func.now())
    modification_date: datetime = db.Column(db.DateTime(timezone=True), onupdate=func.now())
