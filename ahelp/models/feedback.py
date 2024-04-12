from datetime import datetime

from sqlalchemy import func

from ahelp.extensions import db


class FeedbackModel(db.Model):
    """Basic model of data feedback data received when sending messages"""

    __tablename__ = "Feedback data"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String(100), nullable=False)
    number: str = db.Column(db.String(15), nullable=True)
    mail: str = db.Column(db.String(100), nullable=False)
    message: str = db.Column(db.String(1000), nullable=False)
    date: datetime = db.Column(db.DateTime(timezone=True), server_default=func.now())
