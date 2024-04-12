from datetime import datetime

from sqlalchemy import func

from ahelp.extensions import db


class PaymentModel(db.Model):
    """Basic model of of data for payment block"""

    __tablename__ = "Payment"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    photo_path: str = db.Column(db.String)
    header: str = db.Column(db.String(100))
    header_en: str = db.Column(db.String(100))
    body: str = db.Column(db.String(600))
    body_en: str = db.Column(db.String(600))
    title: str = db.Column(db.String(100))
    title_en: str = db.Column(db.String(100))
    description: str = db.Column(db.String(600))
    description_en: str = db.Column(db.String(600))
    creation_date: datetime = db.Column(db.DateTime(timezone=True), server_default=func.now())
    modification_date: datetime = db.Column(db.DateTime(timezone=True), onupdate=func.now())
