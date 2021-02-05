import os
import unittest


class FileStorageTest(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        notes_path = os.path.join(os.getcwd(), "notes_stubs")
        print(notes_path)
        # self.fs = Filestorage()

    def test_it_(self):
        self.assertEqual(True, True)
