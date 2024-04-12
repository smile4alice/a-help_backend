from ahelp.models import User
from ahelp.extensions import ma, db


class UserSchema(ma.SQLAlchemyAutoSchema):
    id: int = ma.Int(dump_only=True)
    password: str = ma.String(load_only=True, required=True)

    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True
        exclude = ("password",)
