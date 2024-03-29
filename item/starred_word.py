from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from models.recent_search import create_recent_search
from models.starred_word import destroy_starred_word
from shared.font_settings import FontSettings

import gettext

class StarredWord(QWidget):
  def __init__(self, word):
    super().__init__()

    from menu.settings import Settings
    language_code = Settings.get_setting('language')
    language = gettext.translation('item', localedir='resources/locale', languages=[language_code])
    language.install()
    _ = language.gettext

    self.setFixedHeight(50)

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.layout.setSpacing(0)

    font = FontSettings.get_font('single_word')

    data_widget = QWidget()
    data_widget.layout = QHBoxLayout(data_widget)
    data_widget.layout.setContentsMargins(0, 0, 0, 0)
    data_widget.layout.setSpacing(10)

    self.word = QLabel(word)
    self.word.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    self.word.setFont(font)

    reload_button = QPushButton()
    reload_button.setIcon(QIcon('resources/search.png'))
    reload_button.setToolTip(_('RELOAD_TEXT'))
    reload_button.clicked.connect(self.reload_word)
    reload_button.setFixedWidth(30)

    self.star_button = QPushButton()
    self.star_button.setToolTip(_('UNSTAR_TEXT'))
    self.star_button.clicked.connect(self.toggle_starred_state)
    self.star_button.setFixedWidth(30)
    self.star_button.setIcon(QIcon('resources/starred.svg'))

    line = QFrame()
    line.setFrameShape(QFrame.Shape.HLine)
    line.setFrameShadow(QFrame.Shadow.Plain)

    data_widget.layout.addSpacing(5)
    data_widget.layout.addWidget(self.word)
    data_widget.layout.addWidget(reload_button)
    data_widget.layout.addWidget(self.star_button)
    data_widget.layout.addSpacing(10)

    self.layout.addWidget(data_widget)
    self.layout.addWidget(line)

    self.style()

  def style(self):
    from shared.styles import Styles
    self.setStyleSheet(Styles.item_widgets_style)

  def toggle_starred_state(self):
    word = self.word.text()

    from side.recent_searches_widget import RecentSearchesWidget
    RecentSearchesWidget.toggle_recent_search_starred_icon(word)

    destroy_starred_word(word)
    self.remove_word()

  def remove_word(self):
    from side.starred_words_widget import StarredWordsWidget
    StarredWordsWidget.remove_starred_word(self)

    self.hide()
    self.deleteLater()

  def reload_word(self):
    word = self.word.text()

    from central.main_widget import MainWidget
    from side.recent_searches_widget import RecentSearchesWidget
    MainWidget.search_word(word)

    recent_search_exists = create_recent_search(word)
    if recent_search_exists:
      RecentSearchesWidget.remove_and_add_recent_search(word)
    else:
      RecentSearchesWidget.add_recent_search(word)

  def update_word(self, new_word):
    self.word.setText(new_word)
