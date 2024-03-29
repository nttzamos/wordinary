from PyQt6.QtWidgets import QLabel, QScrollArea, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

from item.starred_word import StarredWord
from menu.settings import Settings
from models.starred_word import get_starred_words
from shared.font_settings import FontSettings
from shared.spacer import Spacer

import gettext

language_code = Settings.get_setting('language')
language = gettext.translation('side', localedir='resources/locale', languages=[language_code])
language.install()
_ = language.gettext

class StarredWordsWidget(QWidget):
  def __init__(self):
    super().__init__()

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.layout.setSpacing(0)

    StarredWordsWidget.starred_words_list = QWidget()
    StarredWordsWidget.starred_words_list.layout = QVBoxLayout(StarredWordsWidget.starred_words_list)
    StarredWordsWidget.starred_words_list.layout.setSpacing(0)
    StarredWordsWidget.starred_words_list.layout.setContentsMargins(0, 0, 0, 0)

    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setWidget(StarredWordsWidget.starred_words_list)
    scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

    StarredWordsWidget.widget_list = []

    font = FontSettings.get_font('heading')

    title_label = QLabel(_('STARRED_WORDS_TITLE'))
    title_label.setFont(font)
    title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    from shared.styles import Styles
    title_label.setStyleSheet(Styles.side_widgets_title_label_style)

    StarredWordsWidget.placeholder_label = QLabel()
    StarredWordsWidget.placeholder_label.setFont(font)
    StarredWordsWidget.placeholder_label.setWordWrap(True)
    StarredWordsWidget.placeholder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    StarredWordsWidget.show_placeholder_label = False

    StarredWordsWidget.spacer = Spacer()

    self.layout.addWidget(title_label)
    self.layout.addWidget(scroll_area)

    self.setMinimumWidth(Settings.get_setting('left_widget_width'))

    self.style()

  def style(self):
    from shared.styles import Styles
    self.setStyleSheet(Styles.side_widgets_style)

  @staticmethod
  def initialize():
    StarredWordsWidget.starred_words_list.layout.insertWidget(0, StarredWordsWidget.spacer)
    StarredWordsWidget.show_placeholder()

  @staticmethod
  def populate():
    StarredWordsWidget.clear_previous_starred_words()

    starred_words = get_starred_words()

    if len(starred_words) == 0:
      StarredWordsWidget.show_placeholder(_('NO_STARRED_WORDS_TEXT'))
      return
    else:
      StarredWordsWidget.hide_placeholder()

    for word in starred_words:
      starred_word = StarredWord(word)
      StarredWordsWidget.widget_list.append(starred_word)
      StarredWordsWidget.starred_words_list.layout.insertWidget(0, starred_word)

  @staticmethod
  def add_starred_word(word):
    if StarredWordsWidget.show_placeholder_label:
      StarredWordsWidget.hide_placeholder()

    starred_word = StarredWord(word)
    StarredWordsWidget.widget_list.append(starred_word)
    length = len(StarredWordsWidget.widget_list)

    StarredWordsWidget.starred_words_list.layout.insertWidget(0, StarredWordsWidget.widget_list[length-1])

  @staticmethod
  def remove_starred_word(starred_word):
    StarredWordsWidget.widget_list.remove(starred_word)
    if len(StarredWordsWidget.widget_list)==0:
      StarredWordsWidget.show_placeholder(_('NO_STARRED_WORDS_TEXT'))

  @staticmethod
  def toggle_starred_word_starred_state(word):
    for starred_word in StarredWordsWidget.widget_list:
      if word == starred_word.word.text():
        starred_word.remove_word()
        return

  @staticmethod
  def clear_previous_starred_words():
    for starred_word in StarredWordsWidget.widget_list:
      starred_word.hide()
      starred_word.deleteLater()

    StarredWordsWidget.widget_list = []
    StarredWordsWidget.show_placeholder()

  @staticmethod
  def show_placeholder(text=None):
    if text == None: text = _('STARRED_WORDS_SHOWN_HERE')

    StarredWordsWidget.placeholder_label.setText(text)

    if not StarredWordsWidget.show_placeholder_label:
      StarredWordsWidget.show_placeholder_label = True
      StarredWordsWidget.starred_words_list.layout.insertWidget(0, StarredWordsWidget.placeholder_label)
      StarredWordsWidget.starred_words_list.layout.removeWidget(StarredWordsWidget.spacer)
      StarredWordsWidget.placeholder_label.show()

  @staticmethod
  def hide_placeholder():
    if StarredWordsWidget.show_placeholder_label:
      StarredWordsWidget.show_placeholder_label = False
      StarredWordsWidget.starred_words_list.layout.insertWidget(0, StarredWordsWidget.spacer)
      StarredWordsWidget.placeholder_label.hide()

  @staticmethod
  def update_word(word, new_word):
    for starred_word in StarredWordsWidget.widget_list:
      if word == starred_word.word.text():
        starred_word.update_word(new_word)
        return

  @staticmethod
  def delete_word(word):
    for starred_word in StarredWordsWidget.widget_list:
      if word == starred_word.word.text():
        starred_word.hide()
        starred_word.deleteLater()
        StarredWordsWidget.remove_starred_word(starred_word)
        return
