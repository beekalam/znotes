class FileStorage:
    def __init__(self, notes_path) -> None:
        super().__init__()
        self.notes_path = notes_path

    def addNote(self, content):
        pass

    def removeNote(self, note_id):
        pass

    def getNote(self, note_id):
        pass

    def searchNotes(self, query):
        pass
