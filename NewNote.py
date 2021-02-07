import sys

from PyQt5 import QtWidgets
from PyQt5.Qt import QApplication
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow, QWidget, QPlainTextEdit, QLineEdit, QPushButton, QVBoxLayout

from FileStorage import FileStorage

NOTES_PATH = "/home/moh/Documents/notes/zettle_notes"


class NewNote(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mainWidget = QWidget()
        self.setMinimumSize(QSize(440, 240))
        self.setWindowTitle("New Note")
        self.fs = FileStorage(NOTES_PATH)
        vbox = QVBoxLayout()

        # title
        self.title = QLineEdit(self)
        vbox.addWidget(self.title)

        # tags
        self.tag = QLineEdit(self)
        self.tag.resize(400, 40)
        vbox.addWidget(self.tag)

        # Add text field
        self.content = QPlainTextEdit(self)
        self.content.insertPlainText(QApplication.clipboard().text())
        self.content.resize(400, 200)
        vbox.addWidget(self.content)

        # button
        self.save_btn = QPushButton('Save', self)
        self.save_btn.resize(400, 40)
        self.save_btn.clicked.connect(self.save_btn_click)
        vbox.addWidget(self.save_btn)

        self.mainWidget.setLayout(vbox)
        self.setCentralWidget(self.mainWidget)

    def save_btn_click(self):
        title = self.title.text()
        content = self.content.toPlainText()
        tag = self.tag.text()
        if len(title.strip()) > 0:
            self.save(title, content, tag)
            self.content.clear()
            self.title.clear()
            self.tag.clear()

    def save(self, title, content, tag):
        # filename = "{} {}.md".format(datetime.now().strftime("%Y%m%d%H%M"), title)
        # path = os.path.join(NOTES_PATH, filename)
        # save_note(title, content, tag, path)
        self.fs.addNote(title, content, tag)

    # Get the system clipboard contents
    def clipboardChanged(self):
        text = QApplication.clipboard().text()
        self.b.insertPlainText(text + '\n')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = NewNote()

    window.show()
    app.exec_()
