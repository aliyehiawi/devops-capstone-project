"""
Account Model
"""
import logging
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

logger = logging.getLogger()
db = SQLAlchemy()


def init_db(app):
    """Initialize the SQLAlchemy app"""
    Account.init_db(app)


class DataValidationError(Exception):
    """Used for data validation errors when deserializing"""


class Account(db.Model):
    """Class that represents an Account."""

    app = None

    # Schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    address = db.Column(db.String(256))
    phone_number = db.Column(db.String(32), nullable=True)
    date_joined = db.Column(db.Date, nullable=False, server_default=func.now())

    def __repr__(self):
        return f"<Account {self.name} id=[{self.id}]>"

    def serialize(self) -> dict:
        """Serializes the Account as a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "phone_number": self.phone_number,
            "date_joined": self.date_joined.isoformat() if self.date_joined else None,
        }

    def deserialize(self, data: dict):
        """Sets attributes from a dictionary"""
        try:
            self.name = data["name"]
            self.email = data["email"]
            self.address = data["address"]
            self.phone_number = data.get("phone_number")
            joined = data.get("date_joined")
            if joined:
                self.date_joined = date.fromisoformat(joined)
        except KeyError as error:
            raise DataValidationError(f"Invalid Account: missing {error.args[0]}") from error
        except TypeError as error:
            raise DataValidationError("Invalid Account: bad or no data") from error
        return self

    def create(self):
        """Creates an Account in the database"""
        logger.info("Creating %s", self.name)
        self.id = None
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Updates an Account in the database"""
        logger.info("Saving %s", self.name)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        """Removes an Account from the database"""
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    ######################
    # CLASS METHODS
    ######################

    @classmethod
    def init_db(cls, app):
        """Initializes the database session (idempotent)"""
        logger.info("Initializing database")
        cls.app = app
        if "sqlalchemy" not in app.extensions:
            db.init_app(app)
        app.app_context().push()
        db.create_all()

    @classmethod
    def all(cls) -> list:
        """Returns all of the Accounts in the database"""
        logger.info("Processing all Accounts")
        return cls.query.all()

    @classmethod
    def find(cls, account_id: int):
        """Finds an Account by its ID"""
        logger.info("Processing lookup for id %s ...", account_id)
        return cls.query.get(account_id)
