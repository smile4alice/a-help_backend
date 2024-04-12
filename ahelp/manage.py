import click
from flask.cli import with_appcontext


@click.command("init")
@with_appcontext
def init():
    """Create a new admin user"""
    import os
    from ahelp.extensions import db, pwd_context
    from ahelp.models import User

    click.echo("create default users")
    salt = os.getenv("SECRET_KEY").encode("utf-8")
    default_user = User(
        username=os.getenv("USER_DEFAULT_LOGIN"),
        password=pwd_context.hash(os.getenv("USER_DEFAULT_PASSWORD"), salt=salt),
        active=True,
        admin=False,
    )
    default_admin = User(
        username=os.getenv("ADMIN_DEFAULT_LOGIN"),
        password=pwd_context.hash(os.getenv("ADMIN_DEFAULT_PASSWORD"), salt=salt),
        active=True,
        admin=True,
    )

    db.session.add(default_user)
    db.session.add(default_admin)
    db.session.commit()
    click.echo("created default users")
