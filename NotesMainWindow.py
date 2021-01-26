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
        self.list = QListWidget()
        self.web_view = QWebEngineView()
        self.noteContent = QPlainTextEdit()
        self.tab_bar = QTabWidget(self)
        self.search = QLineEdit(self)
        self.prev_note = None
        self.current_note = None
        self.InitializeUI()

    def InitializeUI(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle("Notes List")

        self.createSearchWidget()
        self.createNotePreview()
        self.createNoteList()


        self.show()

    def createSearchWidget(self):
        dock_widget = QDockWidget()
        dock_widget.setWindowTitle('example dock')
        dock_widget.setAllowedAreas(Qt.AllDockWidgetAreas)

        self.search.returnPressed.connect(self.doSearch)
        self.search.setFixedHeight(50)
        dock_widget.setWidget(self.search)

        self.addDockWidget(Qt.LeftDockWidgetArea, dock_widget)

    def createNotePreview(self):

        self.tab_bar.addTab(self.noteContent, "note")

        self.web_view.setHtml("")
        self.tab_bar.addTab(self.web_view, "preview")
        self.setCentralWidget(self.tab_bar)

    def createNoteList(self):
        dock_widget = QDockWidget()
        dock_widget.setWindowTitle('example dock')
        dock_widget.setAllowedAreas(Qt.AllDockWidgetAreas)

        dock_widget.setWidget(self.list)
        for i, path in enumerate(build_file_list()):
            self.list.insertItem(i, path)
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


App = QApplication(sys.argv)
window = Notes()
sys.exit(App.exec())
