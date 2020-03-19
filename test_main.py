import unittest
from main import old_posts, stream

class TestOldPosts(unittest.TestCase):
    # old_posts returns True when complete
    def test_post(self):
        self.assertEqual(old_posts(), True)

# Can't test stream() since it never ends?
