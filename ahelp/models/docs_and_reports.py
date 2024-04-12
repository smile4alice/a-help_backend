from datetime import datetime

from sqlalchemy import func

from ahelp.extensions import db


class DocsAndReportsModel(db.Model):
    """Basic model of data for docs and reports block"""

    __tablename__ = "Docs and reports"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    statutes: str = db.Column(db.String)
    ownership_structure: str = db.Column(db.String)
    photo_path: str = db.Column(db.String)
    bank_account_holder_certificate: str = db.Column(db.String)
    certificate_of_nonprofit_organization: str = db.Column(db.String)
    extract_from_unified_state_register: str = db.Column(db.String)
    annual_report: str = db.Column(db.String)
    privacy_policy: str = db.Column(db.String)
    privacy_policy_en: str = db.Column(db.String)
    creation_date: datetime = db.Column(db.DateTime(timezone=True), server_default=func.now())
    modification_date: datetime = db.Column(db.DateTime(timezone=True), onupdate=func.now())
