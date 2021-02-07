import os
from datetime import datetime


class FileStorage:
    def __init__(self, notes_path) -> None:
        super().__init__()
        self.notes_path = notes_path
        self.notes = {}

    def all(self):
        for root, dirs, files in os.walk(self.notes_path):
            for file in files:
                self.notes[file] = os.path.join(root, file)
        return self.notes

    def addNote(self, title: str, content: str, tags: str) -> None:
        content = "{} {}".format(content, os.linesep)
        tags = ' '.join(['#' + t.strip() for t in tags.split()])
        tags = "tags= {} {}".format(tags, os.linesep + os.linesep)
        with open(self._buildFileName(title), 'w') as f:
            f.writelines([self._buildTitle(title), tags, content])

    def _buildFileName(self, title: str) -> str:
        filename = "{} {}.md".format(datetime.now().strftime("%Y%m%d%H%M"), title)
        return os.path.join(self.notes_path, filename)

    def _buildTitle(self, title: str) -> str:
        return "# {} {}".format(title, os.linesep + os.linesep)

    def removeNote(self, note_id):
        pass

    def getNote(self, note_id):
        pass

    def searchNotes(self, query):
        pass
