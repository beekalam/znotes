import os
from datetime import datetime

from utils import read_file_content, read_tags, search_file_content, file_put_content


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

    def getNotes(self):
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

    def _hasNote(self, note_id):
        return note_id in self.notes.keys()

    def getNote(self, note_id):
        if self._hasNote(note_id):
            return read_file_content(self.notes[note_id])

    def searchNotes(self, query):
        """Search in files"""
        terms = [q for q in query.split(':') if not q.startswith('#')]
        search_tags = [q.replace('#', '') for q in query.split(':') if q.startswith('#')]

        res = {}
        for file, file_path in self.all().items():
            # print(file, file_path)
            file_tags = read_tags(file_path)
            if len(search_tags) == 0 or any([search_tag in file_tags for search_tag in search_tags]):
                if len(terms):
                    s = search_file_content(file_path, terms)
                    if s:
                        res[file] = file_path
                else:
                    res[file] = file_path
        self.notes.clear()
        self.notes = res

    def _noteChanged(self, note_id, new_content):
        return self._hasNote(note_id) and self.getNote(note_id) != new_content

    def updateNote(self, note_id, new_content):
        if self._noteChanged(note_id, new_content):
            file_put_content(self.notes[note_id], new_content)
