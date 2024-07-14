import unittest
from datetime import date, timedelta
from models.contact import Contact
from models.user import User
from dependencies.database import SessionLocal, engine, Base

class TestContactRepository(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(bind=engine)
        self.session = SessionLocal()

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(bind=engine)

    def test_delete_contact(self):
        user = User(id=1, username="johndoe", email="john@example.com", full_name="John Doe", hashed_password="hashed", is_active=True)
        self.session.add(user)
        self.session.commit()
        contact = Contact(id=1, first_name="John", last_name="Doe", owner_id=user.id)
        self.session.add(contact)
        self.session.commit()

        self.session.delete(contact)
        self.session.commit()

        result = self.session.query(Contact).filter_by(id=1).first()
        self.assertIsNone(result)

    def test_get_contact(self):
        user = User(id=1, username="johndoe", email="john@example.com", full_name="John Doe", hashed_password="hashed", is_active=True)
        self.session.add(user)
        self.session.commit()
        contact = Contact(id=1, first_name="John", last_name="Doe", owner_id=user.id)
        self.session.add(contact)
        self.session.commit()

        result = self.session.query(Contact).filter_by(id=1).first()
        self.assertIsNotNone(result)
        self.assertEqual(result.first_name, "John")

    def test_get_contacts(self):
        user = User(id=1, username="johndoe", email="john@example.com", full_name="John Doe", hashed_password="hashed", is_active=True)
        self.session.add(user)
        self.session.commit()
        contacts = [
            Contact(id=1, first_name="John", last_name="Doe", owner_id=user.id),
            Contact(id=2, first_name="Jane", last_name="Doe", owner_id=user.id)
        ]
        self.session.add_all(contacts)
        self.session.commit()

        result = self.session.query(Contact).all()
        self.assertEqual(len(result), 2)

    def test_get_upcoming_birthdays(self):
        user = User(id=1, username="johndoe", email="john@example.com", full_name="John Doe", hashed_password="hashed", is_active=True)
        self.session.add(user)
        self.session.commit()
        contacts = [
            Contact(id=1, first_name="John", last_name="Doe", birthday=date.today() + timedelta(days=1), owner_id=user.id),
            Contact(id=2, first_name="Jane", last_name="Doe", birthday=date.today() + timedelta(days=2), owner_id=user.id)
        ]
        self.session.add_all(contacts)
        self.session.commit()

        result = self.session.query(Contact).filter(Contact.birthday >= date.today()).all()
        self.assertEqual(len(result), 2)

    def test_search_contacts(self):
        user = User(id=1, username="johndoe", email="john@example.com", full_name="John Doe", hashed_password="hashed", is_active=True)
        self.session.add(user)
        self.session.commit()
        contacts = [
            Contact(id=1, first_name="John", last_name="Doe", owner_id=user.id),
            Contact(id=2, first_name="Jane", last_name="Doe", owner_id=user.id)
        ]
        self.session.add_all(contacts)
        self.session.commit()

        result = self.session.query(Contact).filter(Contact.first_name.like("%John%")).all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].first_name, "John")

if __name__ == '__main__':
    unittest.main()
