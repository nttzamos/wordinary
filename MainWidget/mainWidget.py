from typing import Set
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QSizePolicy, QVBoxLayout, QWidget
from MainWidget.currentSearch import CurrentSearch

from databaseHandler import DBHandler
from SideWidgets.recentSearchesWidget import RecentSearchesWidget
from MainWidget.searchingWidget import SearchingWidget
from MainWidget.resultsWidget import ResultsWidget
from MainWidget.result import Result
from settings import Settings

class MainWidget(QWidget):
  searchingWidget = SearchingWidget()
  currentSearch = CurrentSearch()
  resultsWidget = ResultsWidget()

  def __init__(self):
    super().__init__()
    self.layout = QVBoxLayout(self)
    self.layout.setSpacing(0)
    self.layout.setContentsMargins(0, 0, 0, 0)

    self.layout.addWidget(MainWidget.searchingWidget)
    self.layout.addWidget(MainWidget.currentSearch)
    self.layout.addWidget(MainWidget.resultsWidget)

    self.setMinimumWidth(Settings.rightWidgetWidth)

  def findMinimumSize(self):
    longResult = Result("123456789012345678901234")
    return longResult.sizeHint().width()

  @staticmethod
  def addWord(word):
    if (word != MainWidget.currentSearch.getCurrentWord()):
      MainWidget.currentSearch.searchedWord.setText(word)
      ResultsWidget.showResults(word)