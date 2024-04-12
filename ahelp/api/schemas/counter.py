from datetime import datetime

from ahelp.models import CounterModel
from ahelp.extensions import ma, db


class CounterSchema(ma.SQLAlchemyAutoSchema):
    id: int = ma.Integer(dump_only=True)
    currency_symbol: str = ma.String(required=True)
    amount: str = ma.Integer(required=True)
    locale: str = ma.String(required=True)
    creation_date: datetime = ma.DateTime(dump_only=True)
    modification_date: datetime = ma.DateTime(dump_only=True)

    class Meta:
        model = CounterModel
        sqla_session = db.session
        load_instance = True
