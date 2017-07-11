import unittest
from bucketapp.models.user.user import User


class TestActivity(unittest.TestCase):
    def test_is_type(self):
        new_user = User('john doe', 'jdoe@test.com', 'password')
        self.assertIsInstance(new_user, User)