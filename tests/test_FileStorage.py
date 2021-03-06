import os
import unittest
from datetime import datetime

from FileStorage import FileStorage
from utils import file_put_content, file_exists, read_file_content


class FileStorageTest(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.notes_path = os.path.join(os.getcwd(), "tests", "notes_stubs")

    def _clean_stub_files(self):
        # clean test stubs
        for root, dirs, files in os.walk(self.notes_path):
            for file in files:
                os.remove(os.path.join(root, file))

    def setUp(self) -> None:
        super().setUp()
        self._clean_stub_files()
        # create test notes
        self.notes = {}
        self.notes["202006151711 online coding tools.md"] = """
# online coding tools
tags = #bookmark

## ide and Playground
https://codesandbox.io/
https://stephengrider.github.io/playgrounds/"""

        self.notes["202006152336 read from stdin.md"] = """
# read from stdin
tags = #php


```php
<?php
\\ Complete the jumpingOnClouds function below.

function jumpingOnClouds($c) {

}

$fptr = fopen(getenv("OUTPUT_PATH"), "w");
$stdin = fopen("php://stdin", "r");
fscanf($stdin, "%d\n", $n);
fscanf($stdin, "%[^\n]", $c_temp);
$c = array_map('intval', preg_split('/ /', $c_temp, -1, PREG_SPLIT_NO_EMPTY));
$result = jumpingOnClouds($c);
fwrite($fptr, $result . "\n");
fclose($stdin);
fclose($fptr);
```

"""

        for name, content in self.notes.items():
            file_put_content(os.path.join(self.notes_path, name), content)
        self.fs = FileStorage(self.notes_path)

    def tearDown(self) -> None:
        super().tearDown()
        self._clean_stub_files()

    def test_it_can_pull_all_notes(self):
        for k, _ in self.notes.items():
            self.assertTrue(k in self.fs.all().keys())

    def test_it_can_add_note(self):
        title = "this is my note title"
        tags = "math geography"
        self.fs.addNote(title, "this my note content", tags)

        file_name = "{} {}.md".format(datetime.now().strftime("%Y%m%d%H%M"), title)
        expected_note_file_path = os.path.join(self.notes_path, file_name)
        self.assertTrue(file_exists(expected_note_file_path))

    def test_it_should_add_correct_title_to_file(self):
        title = "this is my note title"
        content = "this is my content"
        tags = "math geography"
        self.fs.addNote(title, content, tags)

        file_name = "{} {}.md".format(datetime.now().strftime("%Y%m%d%H%M"), title)
        file_path = os.path.join(self.notes_path, file_name)
        file_content = read_file_content(file_path)
        expected_title = "# {}".format(title)
        self.assertTrue(expected_title in file_content)
        self.assertTrue(content in file_content)
        self.assertTrue(file_name in self.fs.all().keys())

    def test_it_should_add_tags_when_adding_new_note(self):
        title = "this is my note title"
        content = "this is my content"
        tags = "math geography history"
        self.fs.addNote(title, content, tags)

        file_name = "{} {}.md".format(datetime.now().strftime("%Y%m%d%H%M"), title)
        file_path = os.path.join(self.notes_path, file_name)
        file_content = read_file_content(file_path)
        file_tags = "tags= #math #geography #history"
        self.assertTrue(file_tags in file_content)

    def test_it_can_get_note_text_content(self):
        for k in self.notes.keys():
            note_path = os.path.join(self.notes_path, k)
            self.assertEqual(self.fs.getNote(k), read_file_content(note_path))

    def test_it_can_search_notes(self):
        self.fs.searchNotes("#php")
        self.assertEqual(1, len(self.fs.getNotes()))

    def test_it_can_update_a_note(self):
        key = "202006151711 online coding tools.md"
        new_content = """
# new note
this is new note content
        """
        self.fs.updateNote(key, new_content)
        self.assertEqual(new_content, self.fs.getNote(key))


if __name__ == "__main__":
    unittest.main()
