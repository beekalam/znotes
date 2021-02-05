import os
import unittest

from FileStorage import FileStorage
from utils import file_put_content


class FileStorageTest(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        notes_path = os.path.join(os.getcwd(), "notes_stubs")
        # clean test stubs
        for root, dirs, files in os.walk(notes_path):
            for file in files:
                os.remove(os.path.join(root, file))

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
            file_put_content(os.path.join(notes_path, name), content)
        self.fs = FileStorage(notes_path)

    def test_it_can_pull_all_notes(self):
        for k, _ in self.notes.items():
            self.assertTrue(k in self.fs.all().keys())
