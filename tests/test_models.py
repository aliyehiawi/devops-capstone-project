"""
Test cases for Account Model
"""
import os
import logging
import unittest
from service import app
from service.models import Account, DataValidationError, db
from tests.factories import AccountFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)


######################################################################
#  Account   M O D E L   T E S T   C A S E S
######################################################################
class TestAccount(unittest.TestCase):
    """Test Cases for Account Model"""

    @classmethod
    def setUpClass(cls):
        """Connect and create tables"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Account.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Disconnect"""
        db.session.close()

    def setUp(self):
        """Truncate before each test"""
        db.session.query(Account).delete()
        db.session.commit()

    def tearDown(self):
        """Cleanup"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################
    def test_create_an_account(self):
        """It should Create an Account and assert that it exists"""
        fake_account = AccountFactory()
        account = Account(
            name=fake_account.name,
            email=fake_account.email,
            address=fake_account.address,
            phone_number=fake_account.phone_number,
            date_joined=fake_account.date_joined,
        )
        self.assertIsNotNone(account)
        self.assertEqual(account.name, fake_account.name)

    def test_add_account(self):
        """It should Add an Account to the database"""
        accounts = Account.all()
        self.assertEqual(accounts, [])
        account = AccountFactory()
        account.create()
        self.assertIsNotNone(account.id)
        accounts = Account.all()
        self.assertEqual(len(accounts), 1)

    def test_read_account(self):
        """It should Read an Account"""
        account = AccountFactory()
        account.create()
        found = Account.find(account.id)
        self.assertEqual(found.id, account.id)
        self.assertEqual(found.name, account.name)

    def test_update_account(self):
        """It should Update an Account"""
        account = AccountFactory()
        account.create()
        account.name = "New Name"
        account.update()
        found = Account.find(account.id)
        self.assertEqual(found.name, "New Name")

    def test_update_account_no_id(self):
        """It should not Update an Account with no id"""
        account = AccountFactory()
        account.id = None
        self.assertRaises(DataValidationError, account.update)

    def test_delete_account(self):
        """It should Delete an Account"""
        account = AccountFactory()
        account.create()
        self.assertEqual(len(Account.all()), 1)
        account.delete()
        self.assertEqual(len(Account.all()), 0)

    def test_list_all_accounts(self):
        """It should List all Accounts"""
        for _ in range(5):
            AccountFactory().create()
        self.assertEqual(len(Account.all()), 5)

    def test_find_account(self):
        """It should Find an Account by ID"""
        accounts = []
        for _ in range(5):
            account = AccountFactory()
            account.create()
            accounts.append(account)
        account = accounts[2]
        found = Account.find(account.id)
        self.assertIsNotNone(found)
        self.assertEqual(found.id, account.id)

    def test_serialize(self):
        """It should Serialize an Account"""
        account = AccountFactory()
        serial = account.serialize()
        self.assertIn("name", serial)
        self.assertIn("email", serial)
        self.assertIn("address", serial)
        self.assertIn("phone_number", serial)
        self.assertIn("date_joined", serial)

    def test_deserialize(self):
        """It should Deserialize an Account"""
        data = AccountFactory().serialize()
        account = Account()
        account.deserialize(data)
        self.assertEqual(account.name, data["name"])
        self.assertEqual(account.email, data["email"])

    def test_deserialize_bad_data(self):
        """It should not Deserialize bad data"""
        account = Account()
        self.assertRaises(DataValidationError, account.deserialize, [])

    def test_deserialize_missing_field(self):
        """It should not Deserialize when missing a field"""
        account = Account()
        self.assertRaises(DataValidationError, account.deserialize, {"name": "John"})
