from PyQt6.QtWidgets import QVBoxLayout, QTabWidget, QDialog
from PyQt6.QtGui import QIcon

from dialogs.word_addition_widget import WordAdditionWIdget
from dialogs.word_family_update_widget import WordFamilyUpdateWidget
from dialogs.word_update_widget import WordUpdateWidget
from menu.settings import Settings

import gettext

class WordEditingWidget(QDialog):
  def __init__(self):
    super().__init__()

    language_code = Settings.get_setting('language')
    language = gettext.translation('dialogs', localedir='resources/locale', languages=[language_code])
    language.install()
    _ = language.gettext

    self.setWindowTitle(_('EDIT_WORDS_TEXT'))
    self.setWindowIcon(QIcon('resources/window_icon.png'))
    self.setFixedWidth(Settings.get_setting('screen_width') / 2)

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.layout.setSpacing(0)

    add_word_widget = WordAdditionWIdget()
    self.edit_word_widget = WordUpdateWidget()
    WordEditingWidget.edit_word_family_widget = WordFamilyUpdateWidget()

    self.tab_widget = QTabWidget()
    self.tab_widget.addTab(add_word_widget, _('ADD_WORD_TEXT'))
    self.tab_widget.addTab(self.edit_word_widget, _('EDIT_WORD_TEXT'))
    self.tab_widget.addTab(
      WordEditingWidget.edit_word_family_widget, _('EDIT_FAMILY_TEXT')
    )

    self.layout.addWidget(self.tab_widget)

  def closeEvent(self, event):
    from search.searching_widget import SearchingWidget
    SearchingWidget.update_selected_dictionary()

  def hideEvent(self, event):
    from search.searching_widget import SearchingWidget
    SearchingWidget.update_selected_dictionary()

  def set_current_tab_index(self, index):
    self.tab_widget.setCurrentIndex(index)

  def set_word_to_update(self, word, grade_id):
    self.edit_word_widget.set_word_to_update(word, grade_id)

  @staticmethod
  def update_word_family_update_widget(word, grade_id):
    WordEditingWidget.edit_word_family_widget.update_word_family_update_widget(word, grade_id)
