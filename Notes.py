import os

from PyQt5 import QtGui, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QVBoxLayout, QPlainTextEdit, QLineEdit, \
    QHBoxLayout, QAction, QMainWindow, QDockWidget, QTextEdit, QStatusBar
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import Qt
import sys

from NewNote import NewNote
from utils import build_file_list, search, read_file_content, file_put_content
from PyQt5.QtWebEngineWidgets import QWebEngineView
import markdown
from mdx_gfm import GithubFlavoredMarkdownExtension

styles = """
<style>
.highlight{
    background-color:wheat;
}
</style>
"""


class Notes(QMainWindow):
    def __init__(self):
        super().__init__()
        self.list = QListWidget()
        self.web_view = QWebEngineView()
        self.noteContent = QPlainTextEdit()
        self.tab_bar = QTabWidget(self)
        self.search = QLineEdit(self)
        self.current_note_path = None
        self.InitializeUI()

    def InitializeUI(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle("Notes List")

        self.createSearchWidget()
        self.createNotePreview()
        self.createNoteList()
        self.createMenu()
        self.createStatusBar()

        self.show()

    def create_new_note(self):
        self.dialog = NewNote(self)
        self.dialog.closeEvent = self.onNewNoteClosed
        self.dialog.show()

    def onNewNoteClosed(self, event):
        # todo update notes list here.
        print("in........................")

    def createMenu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')

        self.new_act = QAction('New Note', self)
        self.new_act.setShortcut('Ctrl+N')
        self.new_act.triggered.connect(self.create_new_note)
        file_menu.addAction(self.new_act)

        self.save_act = QAction('Save', self)
        self.save_act.setShortcut('Ctrl+S')
        self.save_act.triggered.connect(self.update_current_note)
        file_menu.addAction(self.save_act)

        self.exit_act = QAction('Exit', self)
        self.exit_act.setShortcut('Ctrl+Q')
        self.exit_act.setStatusTip('Quit program')
        self.exit_act.triggered.connect(self.close)
        file_menu.addAction(self.exit_act)

    def createStatusBar(self):
        self.setStatusBar(QStatusBar(self))

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
            self.update_current_note()
            self.current_note_path = item.text()
            self.statusBar().showMessage(self.current_note_path)
            with open(item.text()) as f:
                content = f.read()
                self.noteContent.clear()
                self.noteContent.setPlainText(content)
                self.update_note_markdown_preview(content)

    def update_note_markdown_preview(self, content):
        markdown_content = markdown.markdown(content, extensions=[GithubFlavoredMarkdownExtension()])
        self.web_view.setHtml(styles + markdown_content)

    def update_current_note(self):
        if self.current_note_path is not None and read_file_content(
                self.current_note_path) != self.noteContent.toPlainText():
            print("writing new content....")
            file_put_content(self.current_note_path, self.noteContent.toPlainText())
            self.update_note_markdown_preview(self.noteContent.toPlainText())

    def doSearch(self):
        self.list.clear()
        if self.search.text() == "":
            for i, path in enumerate(build_file_list()):
                self.list.insertItem(i, path)
        else:
            res = search(self.search.text())
            for i, path in enumerate(res):
                self.list.insertItem(i, path)


if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Notes()
    sys.exit(App.exec())
