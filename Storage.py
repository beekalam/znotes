class Storage:
    def __init__(self, storageImpl) -> None:
        """
        @type storageImpl: FileStorage
        """
        super().__init__()
        self.storageImpl = storageImpl

    def addNote(self, content):
        self.storageImpl.addNote(content)

    def removeNote(self, note_id):
        pass

    def getNote(self, note_id):
        pass

    def searchNotes(self, query):
        pass
