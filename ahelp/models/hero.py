from datetime import datetime

from sqlalchemy import func

from ahelp.extensions import db


class HeroModel(db.Model):
    """Basic model of data for hero block"""

    __tablename__ = "Hero"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    active: bool = db.Column(db.Boolean)
    media_path: str = db.Column(db.String, nullable=False)
    slogan: str = db.Column(db.String(100), nullable=False)
    slogan_en: str = db.Column(db.String(100), nullable=False)
    description: str = db.Column(db.String, nullable=False)
    description_en: str = db.Column(db.String, nullable=False)
    call_to_action: str = db.Column(db.String(600), nullable=False)
    call_to_action_en: str = db.Column(db.String(600), nullable=False)
    creation_date: datetime = db.Column(db.DateTime(timezone=True), server_default=func.now())
    modification_date: datetime = db.Column(db.DateTime(timezone=True), onupdate=func.now())
