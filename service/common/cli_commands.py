"""
Flask CLI Commands
"""
from service import app
from service.models import db


@app.cli.command("db-create")
def db_create():
    """Drops and recreates the tables"""
    db.drop_all()
    db.create_all()
    db.session.commit()
