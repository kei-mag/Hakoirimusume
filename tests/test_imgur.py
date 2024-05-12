import os
import re
import unittest

from hakoirimusume.imgur import delete_from_imgur, upload_as_anonymous


class ImgurTest(unittest.TestCase):
    def test_upload_image(self):
        client_id = input("Client ID: ")
        if m := re.match(r"${(.+)}", client_id):
            client_id = os.getenv(m.group(1))
        with open("docs/icon.jpg", "rb") as f:
            result = upload_as_anonymous(client_id, f.read())
            print(result)
            self.assertTrue(isinstance(result, tuple))

    def test_delete_image(self):
        client_id = input("Client ID: ")
        if m := re.match(r"${(.+)}", client_id):
            client_id = os.getenv(m.group(1))
        delete_hash = input("Delete Hash: ")
        result = delete_from_imgur(client_id, delete_hash)
        print("Result: ", result)
        self.assertTrue(result)
