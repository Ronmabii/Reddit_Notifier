import unittest
from main import old_posts, stream

class TestOldPosts(unittest.TestCase):
    # old_posts returns None by default when complete
    def test_post(self):
        self.assertEqual(old_posts(), None)

# Can't test stream() since it never ends?
# env has to be activated to get imports