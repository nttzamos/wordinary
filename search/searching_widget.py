from PyQt6.QtWidgets import QCompleter, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QSizePolicy
from PyQt6.QtCore import QStringListModel, QTimer, Qt
from PyQt6.QtGui import QFont, QIcon, QKeySequence, QShortcut

from menu.settings import Settings
from models.family import get_words_with_family
from models.recent_search import create_recent_search
from shared.database_handler import get_grades, get_words
from shared.styles import Styles
from side.recent_searches_widget import RecentSearchesWidget

class SearchingWidget(QWidget):
  SEARCH_TEXT = 'Αναζήτηση'
  CLEAR_SEARCH_TEXT = 'Καθαρισμός αναζήτησης'
  UNINITIALIZED_STATE_TEXT = 'Πρέπει να επιλέξετε κάποιο μάθημα πρώτα.'
  PLEASE_ENTER_WORD_TEXT = 'Παρακαλώ εισάγετε μια λέξη.'
  EDIT_WORDS_BUTTON_TEXT = 'Επεξεργασία Λέξεων'
  EDIT_WORDS_TOOLTIP_TEXT = ('Μπορείτε να επεξεργαστείτε τις λέξεις κάθε τάξης, '
                             'καθώς και τις συγγενικές τους λέξεις')

  dictionary_words = []

  line_edit = QLineEdit()

  grades = get_grades()
  grades_mapping = {}
  for i in range(len(grades)):
    grades_mapping[i + 1] = grades[i]

  just_searched_with_enter = False

  def __init__(self):
    super().__init__()

    line_edit_font = QFont(Settings.font, 14)
    completer_font = QFont(Settings.font, 12)
    error_message_font = completer_font

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(20, 10, 20, 0)
    self.layout.setSpacing(0)

    SearchingWidget.line_edit.setFont(line_edit_font)
    SearchingWidget.line_edit.setContentsMargins(0, 1, 0, 1)
    SearchingWidget.line_edit.returnPressed.connect(self.search_with_enter)
    SearchingWidget.line_edit.textChanged.connect(self.search_text_changed)
    self.show_error_message = False

    SearchingWidget.completer = QCompleter(SearchingWidget.dictionary_words)
    SearchingWidget.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    SearchingWidget.completer.activated.connect(self.search_with_click)
    SearchingWidget.completer.popup().setFont(completer_font)
    SearchingWidget.line_edit.setCompleter(SearchingWidget.completer)
    SearchingWidget.line_edit.setPlaceholderText(SearchingWidget.PLEASE_ENTER_WORD_TEXT)

    self.search_bar_widget = QWidget()
    self.search_bar_widget.layout = QHBoxLayout(self.search_bar_widget)
    self.search_bar_widget.layout.setContentsMargins(10, 0, 0, 0)

    self.clear_search_button = QPushButton()
    self.clear_search_button.setToolTip(SearchingWidget.CLEAR_SEARCH_TEXT)
    self.clear_search_button.setIcon(QIcon('resources/clear_search.png'))
    self.clear_search_button.clicked.connect(self.clear_search)
    self.hide_clear_search_button = True
    self.clear_search_button.hide()

    search_button = QPushButton()
    search_button.setToolTip(SearchingWidget.SEARCH_TEXT)
    search_button.setIcon(QIcon('resources/search.png'))
    search_button.clicked.connect(self.search_with_button)

    self.search_bar_widget.layout.setSpacing(0)
    self.search_bar_widget.layout.addWidget(SearchingWidget.line_edit)
    self.search_bar_widget.layout.addWidget(self.clear_search_button)
    self.search_bar_widget.layout.addSpacing(5)
    self.search_bar_widget.layout.addWidget(search_button)
    self.search_bar_widget.layout.addSpacing(10)

    SearchingWidget.error_message = QLabel(SearchingWidget.UNINITIALIZED_STATE_TEXT, self)
    SearchingWidget.error_message.setFont(error_message_font)
    size_policy = SearchingWidget.error_message.sizePolicy()
    size_policy.setRetainSizeWhenHidden(True)
    SearchingWidget.error_message.setSizePolicy(size_policy)
    SearchingWidget.error_message.hide()

    edit_words_button_font = QFont(Settings.font, 14)
    SearchingWidget.edit_words_button = QPushButton(SearchingWidget.EDIT_WORDS_BUTTON_TEXT)
    SearchingWidget.edit_words_button.setToolTip(SearchingWidget.EDIT_WORDS_TOOLTIP_TEXT)
    SearchingWidget.edit_words_button.setFont(edit_words_button_font)
    SearchingWidget.edit_words_button.clicked.connect(self.open_words_editing_widget)
    SearchingWidget.edit_words_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

    self.subwidget = QWidget()
    self.subwidget.layout = QHBoxLayout(self.subwidget)
    self.subwidget.layout.setContentsMargins(5, 10, 0, 0)
    self.subwidget.layout.addWidget(SearchingWidget.error_message, alignment=Qt.AlignmentFlag.AlignTop)
    self.subwidget.layout.addWidget(SearchingWidget.edit_words_button)
    size_policy = SearchingWidget.edit_words_button.sizePolicy()
    size_policy.setRetainSizeWhenHidden(True)
    SearchingWidget.edit_words_button.setSizePolicy(size_policy)

    if not Settings.get_boolean_setting('show_edit_dict_words_button'):
      SearchingWidget.edit_words_button.hide()

    self.layout.addWidget(self.search_bar_widget)
    self.layout.addWidget(self.subwidget)

    self.search_bar_focus_shortcut = QShortcut(QKeySequence('/'), self)
    self.search_bar_focus_shortcut.activated.connect(SearchingWidget.set_focus_to_search_bar)

    self.style()
    self.set_focused_styleSheet()

  def style(self):
    SearchingWidget.error_message.setStyleSheet(Styles.error_message_style)
    self.subwidget.setStyleSheet(Styles.subwidget_style)

  def set_focused_styleSheet(self):
    self.search_bar_widget.setStyleSheet(Styles.searching_widget_focused_style)

  def setUnfocusedStyleSheet(self):
    self.search_bar_widget.setStyleSheet(Styles.searching_widget_unfocused_style)

  def set_error_style_sheet(self):
    self.search_bar_widget.setStyleSheet(Styles.searching_widget_error_style)
    SearchingWidget.error_message.show()

  @staticmethod
  def set_initial_error_message():
    SearchingWidget.error_message.setText(SearchingWidget.UNINITIALIZED_STATE_TEXT)

  @staticmethod
  def modify_error_message(text, single):
    SearchingWidget.error_message.setText(SearchingWidget.unknown_word_message(text, single))

  @staticmethod
  def unknown_word_message(text, single):
    if single:
      return 'Αυτή η λέξη δεν περιλαμβάνεται στις λέξεις του βιβλίου ' + \
        text + '. Παρακαλώ αναζητήστε μια διαφορετική λέξη.'
    else:
      return 'Αυτή η λέξη δεν περιλαμβάνεται στα βιβλία του προφίλ ' + \
        text + '. Παρακαλώ αναζητήστε μια διαφορετική λέξη.'

  @staticmethod
  def toggle_edit_words_button_visibility(new_visibility_status):
    SearchingWidget.edit_words_button.show() if new_visibility_status else SearchingWidget.edit_words_button.hide()

  @staticmethod
  def update_selected_dictionary():
    from search.current_search import CurrentSearch
    if CurrentSearch.subject_selector_active:
      subject_name = CurrentSearch.subject_selector.currentText()

      if Settings.get_boolean_setting('only_show_words_with_family'):
        SearchingWidget.dictionary_words = get_words_with_family(CurrentSearch.profile_id, CurrentSearch.grade_id, subject_name)
      else:
        SearchingWidget.dictionary_words = get_words(CurrentSearch.profile_id, CurrentSearch.grade_id, subject_name)

      model = QStringListModel(SearchingWidget.dictionary_words, SearchingWidget.completer)
      SearchingWidget.completer.setModel(model)

  @staticmethod
  def add_or_remove_dictionary_words(words_to_add, words_to_remove):
    if len(words_to_add) > 0:
      SearchingWidget.dictionary_words.extend(words_to_add)

    if len(words_to_remove) > 0:
      for word in words_to_remove:
        SearchingWidget.dictionary_words.remove(word)

    model = QStringListModel(SearchingWidget.dictionary_words, SearchingWidget.completer)
    SearchingWidget.completer.setModel(model)

  def search_text_changed(self):
    if not self.hide_clear_search_button and not SearchingWidget.line_edit.text():
      self.clear_search_button.hide()
      self.hide_clear_search_button = True
    elif self.hide_clear_search_button and SearchingWidget.line_edit.text():
      self.clear_search_button.show()
      self.hide_clear_search_button = False

    if self.show_error_message:
      self.show_error_message = False
      self.set_focused_styleSheet()
      SearchingWidget.error_message.hide()

  def search_with_enter(self):
    SearchingWidget.just_searched_with_enter = True

    if SearchingWidget.line_edit.text() in SearchingWidget.dictionary_words:
      self.add_recent_search(SearchingWidget.line_edit.text())
      self.clear_search()
    else:
      self.show_error_message = True
      self.set_error_style_sheet()
      SearchingWidget.set_focus_to_search_bar()

  def search_with_button(self):
    if SearchingWidget.line_edit.text() in SearchingWidget.dictionary_words:
      self.add_recent_search(SearchingWidget.line_edit.text())
      self.clear_search()
    else:
      self.show_error_message = True
      self.set_error_style_sheet()
      SearchingWidget.set_focus_to_search_bar()

  def search_with_click(self, text):
    if SearchingWidget.just_searched_with_enter:
      SearchingWidget.just_searched_with_enter = False
      return

    self.add_recent_search(text)
    self.clear_search()

  def clear_search(self):
    QTimer.singleShot(0, SearchingWidget.line_edit.clear)
    SearchingWidget.set_focus_to_search_bar()

  def add_recent_search(self, word):
    from central.main_widget import MainWidget
    MainWidget.add_word(word)

    recent_search_exists = create_recent_search(word)
    if recent_search_exists:
      RecentSearchesWidget.remove_and_add_recent_search(word)
    else:
      RecentSearchesWidget.add_recent_search(word)

  @staticmethod
  def set_focus_to_search_bar():
    SearchingWidget.line_edit.setFocus()

  def open_words_editing_widget(self):
    from dialogs.word_editing_widget import WordEditingWidget
    students_editing_dialog = WordEditingWidget()
    students_editing_dialog.exec()