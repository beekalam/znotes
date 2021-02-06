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

    def addNote(self, title, content, tags):
        filename = "{} {}.md".format(datetime.now().strftime("%Y%m%d%H%M"), title)
        file_path = os.path.join(self.notes_path, filename)
        title = "# {} {}".format(title, os.linesep + os.linesep)
        content = "{} {}".format(content, os.linesep)
        tags = ' '.join(['#' + t.strip() for t in tags.split()])
        tags = "tags= {} {}".format(tags, os.linesep + os.linesep)
        with open(file_path, 'w') as f:
            f.writelines([title, tags, content])

    def removeNote(self, note_id):
        pass

    def getNote(self, note_id):
        pass

    def searchNotes(self, query):
        pass
