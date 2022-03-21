from PyQt6.QtWidgets import QFrame, QSplitter, QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from central.main_widget import MainWidget
from menu.menu_bar import MenuBar
from models.profile import get_profile_name
from side.recent_searches_widget import RecentSearchesWidget
from side.starred_words_widget import StarredWordsWidget

class MainWindow(QWidget):
  def __init__(self):
    super().__init__()

    self.setWindowIcon(QIcon('resources/window_icon.png'))
    self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

    self.layout = QVBoxLayout(self)
    self.layout.setSpacing(0)
    self.layout.setContentsMargins(0, 0, 0, 0)

    self.menu_bar = MenuBar(self)

    vertical_splitter = QSplitter()
    vertical_splitter.setOrientation(Qt.Orientation.Vertical)
    vertical_splitter.setChildrenCollapsible(False)

    MainWindow.recent_searches_widget = RecentSearchesWidget()
    MainWindow.starred_words_widget = StarredWordsWidget()
    MainWindow.main_widget = MainWidget()

    vertical_splitter.addWidget(MainWindow.recent_searches_widget)
    MainWindow.recent_searches_widget.initialize()

    vertical_splitter.addWidget(MainWindow.starred_words_widget)
    MainWindow.starred_words_widget.initialize()

    self.main_window_widget = QWidget(self)
    self.main_window_widget.layout = QHBoxLayout(self.main_window_widget)
    self.main_window_widget.layout.setSpacing(10)
    self.main_window_widget.layout.setContentsMargins(0, 0, 0, 0)
    self.main_window_widget.layout.addWidget(vertical_splitter)
    self.main_window_widget.layout.addWidget(MainWindow.main_widget)

    self.line = QFrame()
    self.line.setFrameShape(QFrame.Shape.HLine)
    self.line.setFrameShadow(QFrame.Shadow.Plain)
    self.line.setFixedHeight(2)

    self.layout.addWidget(self.menu_bar)
    self.layout.addWidget(self.line)
    self.layout.addWidget(self.main_window_widget)

    self.style()

  def style(self):
    self.line.setStyleSheet('QWidget { background-color: none }')

    from shared.styles import Styles
    self.main_window_widget.setStyleSheet(Styles.main_window_background_style)
    self.setStyleSheet(Styles.main_window_style)

  @staticmethod
  def update_widgets(profile_id, subject_name):
    from search.searching_widget import SearchingWidget
    from central.results_widget import ResultsWidget

    if subject_name == MainWidget.current_search.ALL_SUBJECTS_TEXT:
      SearchingWidget.modify_error_message(get_profile_name(profile_id), False)
    else:
      SearchingWidget.modify_error_message(subject_name, True)

    SearchingWidget.update_selected_dictionary()
    ResultsWidget.show_placeholder()
    RecentSearchesWidget.populate()
    StarredWordsWidget.populate()
    MainWidget.current_search.searched_word_label.setText(
      MainWidget.current_search.ENTER_WORD_TEXT
    )

  @staticmethod
  def clear_previous_subject_details():
    from search.current_search import CurrentSearch
    if not CurrentSearch.subject_selector_active: return

    from search.searching_widget import SearchingWidget
    from central.results_widget import ResultsWidget

    CurrentSearch.subject_selector_active = False
    SearchingWidget.dictionary_words = []
    SearchingWidget.completer.setModel(None)
    SearchingWidget.set_initial_error_message()
    ResultsWidget.show_placeholder()
    RecentSearchesWidget.clear_previous_recent_searches()
    StarredWordsWidget.clear_previous_starred_words()
