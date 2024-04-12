from datetime import datetime

from sqlalchemy import func

from ahelp.extensions import db


class CounterModel(db.Model):
    """Basic model of data for counter block"""

    __tablename__ = "Counter"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    currency_symbol: str = db.Column(db.String(20))
    amount: int = db.Column(db.Integer)
    locale: str = db.Column(db.String(100))
    creation_date: datetime = db.Column(db.DateTime(timezone=True), server_default=func.now())
    modification_date: datetime = db.Column(db.DateTime(timezone=True), onupdate=func.now())
