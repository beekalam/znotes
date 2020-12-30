import os

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QLabel, QVBoxLayout, QPlainTextEdit, QLineEdit, \
    QHBoxLayout
import sys

from utils import build_file_list, search, read_file_content, file_put_content


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "PyQt5 QListWidget"
        self.top = 200
        self.left = 500
        self.width = 400
        self.height = 300
        self.prev_note = None
        self.InitWindow()

    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        vbox = QVBoxLayout()

        self.search = QLineEdit(self)
        self.search.returnPressed.connect(self.doSearch)
        self.search.setFixedHeight(50)
        vbox.addWidget(self.search)

        hbox = QHBoxLayout()
        hbox.setSpacing(0)
        hbox.setContentsMargins(0, 0, 0, 0)
        vbox.addLayout(hbox)
        self.list = QListWidget()
        # self.list.setFixedWidth(400)
        for i, path in enumerate(build_file_list()):
            self.list.insertItem(i, path)
        # self.list.clicked.connect(self.listview_clicked)
        self.list.currentRowChanged.connect(self.listview_clicked)
        hbox.addWidget(self.list)

        # self.label = QLabel()
        # self.label.setFont(QtGui.QFont("Sanserif", 15))
        # hbox.addWidget(self.label)

        self.noteContent = QPlainTextEdit()
        # self.noteContent.setFixedWidth(400)
        hbox.addWidget(self.noteContent)

        self.setLayout(vbox)
        self.show()

    def listview_clicked(self):
        item = self.list.currentItem()
        if item is not None and item.text() is not None and os.path.isfile(item.text()):
            if self.prev_note is not None and read_file_content(self.prev_note) != self.noteContent.toPlainText():
                print("writing new content....")
                file_put_content(self.prev_note, self.noteContent.toPlainText())
            self.prev_note = item.text()
            with open(item.text()) as f:
                self.noteContent.clear()
                self.noteContent.setPlainText(f.read())

    def doSearch(self):
        self.list.clear()
        if self.search.text() == "":
            for i, path in enumerate(build_file_list()):
                self.list.insertItem(i, path)
        else:
            res = search(self.search.text())
            for i, path in enumerate(res):
                self.list.insertItem(i, path)
        # terms = self.search.text().split(":")
        # tags = [t.strip('#') for t in terms if t.startswith('#')]
        # print(tags)
        # print(search)


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
