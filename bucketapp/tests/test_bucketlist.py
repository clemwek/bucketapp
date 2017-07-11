import unittest
from bucketapp.models.bucketlist.bucketlist import Bucketlist


class TestActivity(unittest.TestCase):
    def test_is_type(self):
        new_bucketlist= Bucketlist('play pool', 'username')
        self.assertIsInstance(new_bucketlist, Bucketlist)