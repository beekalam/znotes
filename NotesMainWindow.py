import os

from PyQt5 import QtGui, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QVBoxLayout, QPlainTextEdit, QLineEdit, \
    QHBoxLayout, QAction, QMainWindow, QDockWidget, QTextEdit
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import Qt
import sys

from utils import build_file_list, search, read_file_content, file_put_content
from PyQt5.QtWebEngineWidgets import QWebEngineView
import markdown
from mdx_gfm import GithubFlavoredMarkdownExtension


class Notes(QMainWindow):
    def __init__(self):
        super().__init__()
        self.prev_note = None
        self.InitializeUI()

    def InitializeUI(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle("Notes List")

        # set central widget for main window
        self.createSearchWidget()
        self.createCentralWidget()
        self.createDockWidget()

        self.show()

    def createSearchWidget(self):
        dock_widget = QDockWidget()
        dock_widget.setWindowTitle('example dock')
        dock_widget.setAllowedAreas(Qt.AllDockWidgetAreas)

        self.search = QLineEdit(self)
        self.search.returnPressed.connect(self.doSearch)
        self.search.setFixedHeight(50)
        dock_widget.setWidget(self.search)

        self.addDockWidget(Qt.LeftDockWidgetArea, dock_widget)

    def createCentralWidget(self):

        self.tab_bar = QTabWidget(self)
        # self.notes_content_tab = QWidget()
        # self.notes_preview = QWidget()

        self.noteContent = QPlainTextEdit()
        self.tab_bar.addTab(self.noteContent, "note")
        # self.noteContent.setFixedWidth(400)
        # hbox.addWidget(self.noteContent)

        self.web_view = QWebEngineView()
        self.web_view.setHtml("")
        # hbox.addWidget(self.web_view)
        self.tab_bar.addTab(self.web_view, "preview")
        self.setCentralWidget(self.tab_bar)

    def createDockWidget(self):
        dock_widget = QDockWidget()
        dock_widget.setWindowTitle('example dock')
        dock_widget.setAllowedAreas(Qt.AllDockWidgetAreas)

        self.list = QListWidget()
        dock_widget.setWidget(self.list)
        for i, path in enumerate(build_file_list()):
            self.list.insertItem(i, path)
        # self.list.clicked.connect(self.listview_clicked)
        self.list.currentRowChanged.connect(self.listview_clicked)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock_widget)

    def listview_clicked(self):
        item = self.list.currentItem()
        if item is not None and item.text() is not None and os.path.isfile(item.text()):
            if self.prev_note is not None and read_file_content(self.prev_note) != self.noteContent.toPlainText():
                print("writing new content....")
                file_put_content(self.prev_note, self.noteContent.toPlainText())
            self.prev_note = item.text()
            with open(item.text()) as f:
                content = f.read()
                self.noteContent.clear()
                self.noteContent.setPlainText(content)
                self.web_view.setHtml(markdown.markdown(content,
                                                        extensions=[GithubFlavoredMarkdownExtension()]))

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
window = Notes()
sys.exit(App.exec())
