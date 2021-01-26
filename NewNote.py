# PyQt5 clipboard
#
# Gets text from the system clipboard
# If you copy text to the clipboard,
# output is shown in the console.
#
# pythonprogramminglanguage.com
#

import sys
import os
from PyQt5.Qt import QApplication, QClipboard
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QPlainTextEdit, QComboBox, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import QSize
from datetime import datetime

from PyQt5.QtCore import QAbstractNativeEventFilter, QAbstractEventDispatcher

NOTES_PATH = "/home/moh/Documents/notes/zettle_notes"


def build_tags_list():
    def read_tags(path):
        lines = open(path, 'r').read().split("\n")
        res = list(filter(lambda x: x.startswith("tags"), lines))
        if res:
            res = res[0].replace("tags = ", "").replace("#", "").split()
        return res

    tags = []
    for root, dirs, files in os.walk(NOTES_PATH):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                tags.extend(read_tags(path))
    ans = list(set(tags))
    return ans


# class ExampleWindow(QMainWindow):
class NewNote(QWidget):
    def __init__(self):
        super().__init__()
        # QMainWindow.__init__(self)

        self.setMinimumSize(QSize(440, 240))
        self.setWindowTitle("PyQt5 Clipboard example...")
        vbox = QVBoxLayout()

        # title
        self.title = QLineEdit(self)
        # self.title.move(10, 10)
        # self.title.resize(400, 40)
        vbox.addWidget(self.title)

        # tags
        self.tag = QLineEdit(self)
        # self.tag.move(10, 270)
        self.tag.resize(400, 40)
        vbox.addWidget(self.tag)
        # self.tag.addItems(build_tags_list())

        # Add text field
        self.content = QPlainTextEdit(self)
        self.content.insertPlainText(QApplication.clipboard().text())
        # self.content.move(10, 60)
        self.content.resize(400, 200)
        vbox.addWidget(self.content)

        # button
        self.save_btn = QPushButton('Save', self)
        # self.save_btn.move(10, 310)
        self.save_btn.resize(400, 40)
        self.save_btn.clicked.connect(self.save_btn_click)
        vbox.addWidget(self.save_btn)

        self.setLayout(vbox)
        # self.show()
        # save

        # QApplication.clipboard().dataChanged.connect(self.clipboardChanged)

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
        filename = "{} {}.md".format(datetime.now().strftime("%Y%m%d%H%M"), title)
        path = os.path.join(NOTES_PATH, filename)
        title = "# {} {}".format(title, os.linesep + os.linesep)
        tags = ' '.join(['#' + t.strip() for t in tag.split()])
        tags = "tags= {} {}".format(tags, os.linesep + os.linesep)
        content = "{} {}".format(content, os.linesep)
        print(path, tags, content)
        with open(path, 'w') as f:
            f.writelines([title, tags, content])

    # Get the system clipboard contents
    def clipboardChanged(self):
        text = QApplication.clipboard().text()
        print(text)
        self.b.insertPlainText(text + '\n')

    # def buildTags(self):


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = NewNote()

    window.show()
    app.exec_()
