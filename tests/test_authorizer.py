from datetime import datetime
from time import sleep
from unittest import TestCase

from hakoirimusume.authorizer import Authorizer


class TestAuthorizer(TestCase):
    def test_authorize_100times(self):
        authorizer = Authorizer()
        prev_aikotoba = ""
        same_aikotoba_count = 0
        for i in range(100):
            aikotoba = authorizer.create_new_aikotoba("test_user")
            if aikotoba == prev_aikotoba:
                same_aikotoba_count += 1
            else:
                same_aikotoba_count = 0
            prev_aikotoba = aikotoba
            if aikotoba and authorizer.request_user and authorizer.aikotoba and authorizer.expired_time:
                self.assertTrue(authorizer.authorize(aikotoba))
            else:
                raise Exception("Failed to create aikotoba.")
        self.assertLess(same_aikotoba_count, 4)

    def test_wrong_aikotoba(self):
        authorizer = Authorizer()
        aikotoba = authorizer.create_new_aikotoba("test_user")
        if aikotoba and authorizer.request_user and authorizer.aikotoba and authorizer.expired_time:
            self.assertFalse(authorizer.authorize("wrong_aikotoba"))
        else:
            raise Exception("Failed to create aikotoba.")
        self.assertFalse(authorizer.authorize(aikotoba))

    def test_multiple_creation_block(self):
        authorizer = Authorizer()
        aikotoba = authorizer.create_new_aikotoba("test_user")
        self.assertFalse(authorizer.create_new_aikotoba("another_user"))
        self.assertTrue(authorizer.create_new_aikotoba("test_user"))

    def test_expired_aikotoba(self):
        authorizer = Authorizer()
        aikotoba = authorizer.create_new_aikotoba("test_user")
        # print("test_expired_aikotoba: created aikotoba. sleeping...")
        if aikotoba and authorizer.request_user and authorizer.aikotoba and authorizer.expired_time:
            sleep((authorizer.expired_time - datetime.now()).seconds + 1)
        else:
            raise Exception("Failed to create aikotoba.")
        self.assertFalse(authorizer.authorize(aikotoba))
        self.assertIsNone(authorizer.aikotoba)
        self.assertIsNone(authorizer.expired_time)
        self.assertIsNone(authorizer.request_user)


authorizer = Authorizer()
