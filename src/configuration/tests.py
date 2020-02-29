from datetime import datetime, timedelta

from utilities.TestSuite import TestCase

from configuration.models import Chunk

class TestConfiguration(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    # These ought to be added by the initial migration
    def testWelcomeMessage(self):
        chunk = Chunk.objects.get(key="Welcome Message")
        self.assertIsNotNone(chunk)

    def testLoginMessage(self):
        chunk = Chunk.objects.get(key="Login Message")
        self.assertIsNotNone(chunk)
