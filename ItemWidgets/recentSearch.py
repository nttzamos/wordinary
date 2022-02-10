from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtGui import QFont, QIcon

from Common.databaseHandler import DBHandler

class RecentSearch(QWidget):
  def __init__(self, word, is_starred):
    super().__init__()

    self.setFixedHeight(50)

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.layout.setSpacing(0)

    self.data_widget = QWidget()
    self.data_widget.layout = QHBoxLayout(self.data_widget)
    self.data_widget.layout.setContentsMargins(0, 0, 0, 0)

    self.word = QLabel(word)
    from MenuBar.settings import Settings
    font = QFont(Settings.font, 14)
    self.word.setFont(font)

    self.reload_button = QPushButton()
    self.reload_button.setIcon(QIcon('Resources/reload.svg'))
    self.reload_button.clicked.connect(self.reload_word)
    self.reload_button.setFixedWidth(30)

    self.star_button = QPushButton()
    self.star_button.clicked.connect(self.toggle_starred_state)
    self.star_button.setFixedWidth(30)

    self.is_starred = is_starred
    if self.is_starred:
      self.star_button.setIcon(QIcon('Resources/starred.svg'))
    else:
      self.star_button.setIcon(QIcon('Resources/unstarred.svg'))

    self.delete_button = QPushButton()
    self.delete_button.setIcon(QIcon('Resources/delete2.svg'))
    self.delete_button.clicked.connect(self.remove_word)
    self.delete_button.setFixedWidth(30)

    self.line = QFrame()
    self.line.setFrameShape(QFrame.Shape.HLine)
    self.line.setFrameShadow(QFrame.Shadow.Plain)

    self.data_widget.layout.addSpacing(5)
    self.data_widget.layout.addWidget(self.word)
    self.data_widget.layout.addWidget(self.reload_button)
    self.data_widget.layout.addWidget(self.star_button)
    self.data_widget.layout.addWidget(self.delete_button)
    self.data_widget.layout.addSpacing(5)

    self.layout.addWidget(self.data_widget)
    self.layout.addWidget(self.line)

    self.style()

  def style(self):
    from Common.styles import Styles
    self.setStyleSheet(Styles.item_widgets_style)

  def reload_word(self):
    word = self.word.text()
    from MainWidget.mainWidget import MainWidget
    from SideWidgets.recentSearchesWidget import RecentSearchesWidget
    MainWidget.add_word(word)
    DBHandler.add_recent_search(word)
    RecentSearchesWidget.remove_and_add_recent_search(word)

  def toggle_starred_state(self):
    from SideWidgets.starredWordsWidget import StarredWordsWidget
    word = self.word.text()

    if self.is_starred:
      DBHandler.remove_starred_word(word)
      StarredWordsWidget.toggle_starred_word_starred_state(word)
    else:
      DBHandler.add_starred_word(word)
      StarredWordsWidget.add_starred_word(word)

    self.toggle_starred_icon()

  def toggle_starred_icon(self):
    if self.is_starred:
      self.is_starred = False
      self.star_button.setIcon(QIcon('Resources/unstarred.svg'))
    else:
      self.is_starred = True
      self.star_button.setIcon(QIcon('Resources/starred.svg'))

  def remove_word(self):
    from SideWidgets.recentSearchesWidget import RecentSearchesWidget
    DBHandler.remove_recent_search(self.word.text())
    self.hide()
    RecentSearchesWidget.remove_recent_search(self)
    self.deleteLater()
