import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from repositories.user_repository import get_user, get_user_by_email, create_user, verify_user
from models.user import User
from schemas.user import UserCreate

class TestUserRepository(unittest.TestCase):

    def setUp(self):
        self.db = MagicMock(spec=Session)

    def test_get_user(self):
        user = User(id=1, email="test@example.com", hashed_password="hashedpassword")
        self.db.query().filter().first.return_value = user
        result = get_user(self.db, user_id=1)
        self.assertEqual(result, user)

    def test_get_user_by_email(self):
        user = User(id=1, email="test@example.com", hashed_password="hashedpassword")
        self.db.query().filter().first.return_value = user
        result = get_user_by_email(self.db, email="test@example.com")
        self.assertEqual(result, user)

    def test_create_user(self):
        user_create = UserCreate(email="test@example.com", password="password")
        user = User(email="test@example.com", hashed_password="password")
        self.db.add = MagicMock()
        self.db.commit = MagicMock()
        self.db.refresh = MagicMock()
        result = create_user(self.db, user=user_create)
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()
        self.assertEqual(result.email, user.email)

    def test_verify_user(self):
        user = User(id=1, email="test@example.com", hashed_password="hashedpassword", verification_token="token")
        self.db.query().filter().first.return_value = user
        self.db.commit = MagicMock()
        self.db.refresh = MagicMock()
        result = verify_user(self.db, token="token")
        self.assertTrue(result.is_verified)
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

if __name__ == '__main__':
    unittest.main()
