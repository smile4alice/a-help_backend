from ahelp.extensions import db


class User(db.Model):
    """Basic user model"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column("password", db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True)
    admin = db.Column(db.Boolean, default=False)
    description = db.Column(db.String, nullable=True)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.active

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return "<User %s>" % self.username
