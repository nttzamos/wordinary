from PyQt6.QtWidgets import (QGridLayout, QLabel, QScrollArea, QVBoxLayout,
                             QWidget, QMessageBox, QCheckBox, QPushButton,
                             QHBoxLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon

from item.result import Result
from menu.settings import Settings
from models.family import (get_family_id, get_family_words, update_word_family,
                           non_related_word_exists)
from models.word import get_word_id, word_exists
from shared.wiktionary_parser import fetch_word_details

import gettext

language_code = Settings.get_setting('language')
language = gettext.translation('central', localedir='resources/locale', languages=[language_code])
language.install()
_ = language.gettext

class ResultsWidget(QWidget):
  def __init__(self):
    super().__init__()

    self.layout = QVBoxLayout(self)
    self.layout.setSpacing(0)
    self.layout.setContentsMargins(0, 0, 0, 0)

    ResultsWidget.scroll_area_widget_contents = QWidget()
    ResultsWidget.grid_layout = QGridLayout(ResultsWidget.scroll_area_widget_contents)
    ResultsWidget.widget_list = []
    ResultsWidget.show_placeholder_label = True
    ResultsWidget.placeholder_label = QLabel(_('RESULT_DISPLAY_TEXT'))

    font = QFont(Settings.FONT, 18)
    title_font = QFont(Settings.FONT, 22)

    ResultsWidget.placeholder_label.setFont(font)
    ResultsWidget.grid_layout.addWidget(ResultsWidget.placeholder_label)
    ResultsWidget.grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    self.scroll_area = QScrollArea()
    self.scroll_area.setWidgetResizable(True)
    self.scroll_area.setWidget(ResultsWidget.scroll_area_widget_contents)

    ResultsWidget.title_label = QLabel('Αποτελέσματα Αναζήτησης')
    ResultsWidget.title_label.setFont(title_font)
    ResultsWidget.title_label.hide()

    ResultsWidget.legend_button = QPushButton()
    ResultsWidget.legend_button.setIcon(QIcon('resources/question.png'))
    ResultsWidget.legend_button.setToolTip(_('RESULT_EXPLANATION_TOOLTIP'))
    ResultsWidget.legend_button.pressed.connect(self.open_legend)
    ResultsWidget.legend_button.setFixedSize(30, 30)
    size_policy = ResultsWidget.legend_button.sizePolicy()
    size_policy.setRetainSizeWhenHidden(True)
    ResultsWidget.legend_button.setSizePolicy(size_policy)
    ResultsWidget.legend_button.hide()

    ResultsWidget.first_row_widget = QWidget()
    ResultsWidget.first_row_widget.layout = QHBoxLayout(ResultsWidget.first_row_widget)
    ResultsWidget.first_row_widget.layout.setSpacing(0)
    ResultsWidget.first_row_widget.layout.setContentsMargins(20, 10, 20, 20)

    ResultsWidget.first_row_widget.layout.addWidget(ResultsWidget.title_label)
    ResultsWidget.first_row_widget.layout.addWidget(
      ResultsWidget.legend_button, Qt.AlignmentFlag.AlignRight
    )

    self.layout.addWidget(ResultsWidget.first_row_widget)
    self.layout.addWidget(self.scroll_area)

    self.style()

  def style(self):
    from shared.styles import Styles
    self.setStyleSheet(Styles.results_widget_style)
    ResultsWidget.legend_button.setStyleSheet(Styles.legend_button_style)

  def open_legend(self):
    from dialogs.result_explanation_widget import ResultExplanationWidget
    result_explanation_widget = ResultExplanationWidget()
    result_explanation_widget.exec()

  @staticmethod
  def show_results(word):
    ResultsWidget.hide_placeholder()
    ResultsWidget.clear_previous_results()
    ResultsWidget.grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    offline_result_words, online_result_words, show_error = ResultsWidget.get_results(word)

    maximum_results = Settings.get_setting('maximum_results')

    longest_word_offline = len(max(offline_result_words, default='', key=len))
    longest_word_online = len(max(online_result_words, default='', key=len))

    str = ''
    for i in range(max(longest_word_offline, longest_word_online)):
      str = str + 'ω'
    single_result_width = Result(str).sizeHint().width()
    grid_columns = Settings.get_results_widget_columns(single_result_width)

    i = 0
    for word in offline_result_words:
      if i == maximum_results: break
      row = i // grid_columns
      column = i % grid_columns
      result = Result(word, widget_width=single_result_width, saved=True)
      ResultsWidget.widget_list.append(result)
      ResultsWidget.grid_layout.addWidget(result, row, column)
      i += 1

    for word in online_result_words:
      if i == maximum_results: break
      row = i // grid_columns
      column = i % grid_columns
      result = Result(word, widget_width=single_result_width, saved=False)
      ResultsWidget.widget_list.append(result)
      ResultsWidget.grid_layout.addWidget(result, row, column)
      i += 1

    if show_error and not Settings.get_boolean_setting('hide_no_internet_message'):
      ResultsWidget.show_no_internet_message()

    if i == 0:
      ResultsWidget.show_placeholder(_('NO_RESULTS_TEXT'))

  @staticmethod
  def get_results(word):
    from search.current_search import CurrentSearch
    grade_id = CurrentSearch.grade_id
    word_id = get_word_id(grade_id, word)
    family_id = get_family_id(grade_id, word_id)
    offline_result_words = get_family_words(grade_id, family_id)

    if word in offline_result_words:
      offline_result_words.remove(word)

    offline_result_words.sort()

    if Settings.get_boolean_setting('use_wiktionary'):
      try:
        online_family_words, unused = fetch_word_details(word)
      except RuntimeError:
        return offline_result_words, [], True

      online_family_words = list(set(online_family_words) - set(offline_result_words))
      non_related_online_family_words = []

      for online_word in online_family_words:
        if word_exists(grade_id, online_word):
          if non_related_word_exists(word, online_word, grade_id):
            non_related_online_family_words.append(online_word)
          else:
            offline_result_words.append(online_word)
            update_word_family(
              CurrentSearch.grade_id,
              CurrentSearch.searched_word_label.text(), [online_word], []
            )

      online_family_words = list(
        set(online_family_words) - set(offline_result_words) - set(non_related_online_family_words)
      )

      online_family_words.sort()
      offline_result_words.sort()

      return offline_result_words, online_family_words, False
    else:
      return offline_result_words, [], False

  @staticmethod
  def clear_previous_results():
    for result in ResultsWidget.widget_list:
      result.hide()
      result.deleteLater()

    ResultsWidget.widget_list = []

  @staticmethod
  def show_placeholder(text=None):
    if text == None: text = _('RESULT_DISPLAY_TEXT')

    ResultsWidget.placeholder_label.setText(text)
    ResultsWidget.clear_previous_results()
    ResultsWidget.title_label.hide()
    ResultsWidget.legend_button.hide()

    if not ResultsWidget.show_placeholder_label:
      ResultsWidget.show_placeholder_label = True
      ResultsWidget.grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
      ResultsWidget.placeholder_label.show()

  @staticmethod
  def hide_placeholder():
    if ResultsWidget.show_placeholder_label:
      ResultsWidget.show_placeholder_label = False
      ResultsWidget.placeholder_label.hide()
      ResultsWidget.title_label.show()
      ResultsWidget.legend_button.show()

  @staticmethod
  def remove_result(result):
    ResultsWidget.widget_list.remove(result)

    if len(ResultsWidget.widget_list)==0:
      ResultsWidget.show_placeholder(_('NO_RESULTS_TEXT'))

  @staticmethod
  def show_no_internet_message():
    title = _('NO_INTERNET_CONNECTION_TITLE')
    text = _('NO_INTERNET_CONNECTION__TEXT')
    answer = QMessageBox()
    answer.setIcon(QMessageBox.Icon.Critical)
    answer.setText(text)
    answer.setWindowTitle(title)
    answer.setStandardButtons(QMessageBox.StandardButton.Ok)

    check_box = QCheckBox(_('HIDE_MESSAGE_CHECKBOX'))
    check_box.clicked.connect(ResultsWidget.toggle_message_setting)
    check_box.setChecked(False)

    answer.setCheckBox(check_box)
    answer.exec()

  @staticmethod
  def toggle_message_setting(value):
    Settings.set_boolean_setting('hide_no_internet_message', value)

  @staticmethod
  def add_word(word):
    for result in ResultsWidget.widget_list:
      if word == result.word_label.text():
        result.add_word()

  @staticmethod
  def update_word(word, new_word):
    for result in ResultsWidget.widget_list:
      if word == result.word_label.text() or new_word == result.word_label.text():
        ResultsWidget.show_placeholder()
        return

  @staticmethod
  def delete_word(word):
    for result in ResultsWidget.widget_list:
      if result.saved and word == result.word_label.text():
        result.hide()
        result.deleteLater()
        ResultsWidget.remove_result(result)
        return
