from PyQt6.QtWidgets import QVBoxLayout, QTabWidget, QDialog
from PyQt6.QtGui import QIcon

from dialogs.word_addition_widget import WordAdditionWIdget
from dialogs.word_family_update_widget import WordFamilyUpdateWidget
from dialogs.word_update_widget import WordUpdateWidget
from menu.settings import Settings

class WordEditingWidget(QDialog):
  EDIT_WORDS_TEXT = 'Επεξεργασία Λέξεων'
  ADD_WORD_TEXT = 'Προσθήκη Λέξης'
  EDIT_WORD_TEXT = 'Επεξεργασία Λέξης'
  EDIT_FAMILY_TEXT = 'Επεξεργασία Συγγενικών Λέξεων'

  def __init__(self):
    super().__init__()
    self.setWindowTitle(WordEditingWidget.EDIT_WORDS_TEXT)
    self.setWindowIcon(QIcon('resources/window_icon.png'))
    self.setFixedWidth(Settings.get_setting('screen_width') / 2)

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.layout.setSpacing(0)

    add_word_widget = WordAdditionWIdget()
    edit_word_widget = WordUpdateWidget()
    edit_word_family_widget = WordFamilyUpdateWidget()

    tab_widget = QTabWidget()
    tab_widget.addTab(add_word_widget, WordEditingWidget.ADD_WORD_TEXT)
    tab_widget.addTab(edit_word_widget, WordEditingWidget.EDIT_WORD_TEXT)
    tab_widget.addTab(edit_word_family_widget, WordEditingWidget.EDIT_FAMILY_TEXT)

    self.layout.addWidget(tab_widget)

  def closeEvent(self, event):
    from search.searching_widget import SearchingWidget
    SearchingWidget.update_selected_dictionary()

  def hideEvent(self, event):
    from search.searching_widget import SearchingWidget
    SearchingWidget.update_selected_dictionary()