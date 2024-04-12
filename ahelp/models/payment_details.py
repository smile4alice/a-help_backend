from datetime import datetime

from sqlalchemy import func

from ahelp.extensions import db


class PaymentDetailsModel(db.Model):
    """Basic model of alternative payment details"""

    __tablename__ = "Payment Details"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    currency: str = db.Column(db.String(3), nullable=False)
    company_name: str = db.Column(db.String(100), nullable=False)
    iban_code: str = db.Column(db.String(34), nullable=False)
    name_of_bank: str = db.Column(db.String(200), nullable=False)
    bank_address: str = db.Column(db.String(200), nullable=False)
    edrpou_code: str = db.Column(db.String(8), nullable=False)
    swift_code: str = db.Column(db.String(11), nullable=False)
    company_address: str = db.Column(db.String(200), nullable=False)
    correspondent_bank: str = db.Column(db.String(200))
    address_of_correspondent_bank: str = db.Column(db.String(200))
    account_of_the_correspondent_bank: str = db.Column(db.String(200))
    swift_code_of_the_correspondent_bank: str = db.Column(db.String(11))
    creation_date: datetime = db.Column(db.DateTime(timezone=True), server_default=func.now())
    modification_date: datetime = db.Column(db.DateTime(timezone=True), onupdate=func.now())
