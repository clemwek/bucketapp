import unittest
from bucketapp.models.activity.activity import Activity


class TestActivity(unittest.TestCase):
    def test_is_type(self):
        new_activity = Activity('play pool', 'bucketlist1', 'bucket item 1 description', 'date', False)
        self.assertIsInstance(new_activity, Activity)
