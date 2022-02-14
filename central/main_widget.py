from PyQt6.QtWidgets import QVBoxLayout, QWidget

from central.current_search import CurrentSearch
from central.searching_widget import SearchingWidget
from central.results_widget import ResultsWidget
from menu.settings import Settings

class MainWidget(QWidget):
  searching_widget = SearchingWidget()
  current_search = CurrentSearch()
  results_widget = ResultsWidget()

  def __init__(self):
    super().__init__()
    self.layout = QVBoxLayout(self)
    self.layout.setSpacing(0)
    self.layout.setContentsMargins(0, 0, 0, 0)

    self.layout.addWidget(MainWidget.searching_widget)
    self.layout.addWidget(MainWidget.current_search)
    self.layout.addWidget(MainWidget.results_widget)

    self.setMinimumWidth(Settings.get_setting('right_widget_width'))

  @staticmethod
  def add_word(word):
    CurrentSearch.searched_word.setText(word)
    ResultsWidget.show_results(word)