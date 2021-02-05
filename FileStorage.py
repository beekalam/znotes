import os


class FileStorage:
    def __init__(self, notes_path) -> None:
        super().__init__()
        self.notes_path = notes_path
        self.notes = {}

    def all(self):
        for root, dirs, files in os.walk(self.notes_path):
            for file in files:
                self.notes[file] = ""
        return self.notes

    def addNote(self, content):
        pass

    def removeNote(self, note_id):
        pass

    def getNote(self, note_id):
        pass

    def searchNotes(self, query):
        pass
