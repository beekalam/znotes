import os
from datetime import datetime

from utils import read_file_content


class FileStorage:
    def __init__(self, notes_path: str) -> None:
        super().__init__()
        self.notes_path = notes_path
        self.notes = {}
        self.all()

    def all(self):
        for root, dirs, files in os.walk(self.notes_path):
            for file in files:
                self.notes[file] = os.path.join(root, file)
        return self.notes

    def addNote(self, title: str, content: str, tags: str) -> None:
        with open(self._buildFilePath(title), 'w') as f:
            f.writelines([
                self._buildTitleLine(title),
                self._buildTagsLine(tags),
                self._buildContent(content)
            ])

    def _buildFilePath(self, title: str) -> str:
        filename = "{} {}.md".format(datetime.now().strftime("%Y%m%d%H%M"), title)
        return os.path.join(self.notes_path, filename)

    def _buildTitleLine(self, title: str) -> str:
        return "# {} {}".format(title, os.linesep + os.linesep)

    def _buildContent(self, content: str) -> str:
        return "{} {}".format(content, os.linesep)

    def _buildTagsLine(self, tags: str) -> str:
        tags = ' '.join(['#' + t.strip() for t in tags.split()])
        return "tags= {} {}".format(tags, os.linesep + os.linesep)

    def removeNote(self, note_id):
        pass

    def getNote(self, note_id):
        if note_id in self.notes.keys():
            return read_file_content(self.notes[note_id])

    def searchNotes(self, query):
        for _, path in self.notes.items():
            lines = read_file_content(path).split("\n")
            res = list(filter(lambda x: x.startswith("tags"), lines))
            if res:
                res = res[0].replace("tags = ", "").replace("#", "").split()
            print(res)
            return res
        return []
