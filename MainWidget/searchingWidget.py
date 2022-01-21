from PyQt6.QtGui import QFont, QIcon, QKeySequence, QShortcut
from PyQt6.QtWidgets import QCompleter, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QSizePolicy
from PyQt6.QtCore import QStringListModel, QTimer, Qt

from databaseHandler import DBHandler
from SideWidgets.recentSearchesWidget import RecentSearchesWidget
from wordsEditingWidget import WordsEditingWidget
from settings import Settings
from styles import Styles

class SearchingWidget(QWidget):
  dictionaryWords = []

  lineEdit = QLineEdit()

  from databaseHandler import DBHandler
  grades = DBHandler.getGrades()
  gradesMapping = {}
  for i in range(len(grades)):
    gradesMapping[i + 1] = grades[i]

  uninitializedStateText = "You have to select a grade first."

  def __init__(self):
    super().__init__()

    lineEditFont = QFont(Settings.font, 14)
    completerFont = QFont(Settings.font, 10)
    errorMessageFont = completerFont

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(20, 10, 20, 0)
    self.layout.setSpacing(5)

    SearchingWidget.lineEdit.setFont(lineEditFont)
    SearchingWidget.lineEdit.setContentsMargins(0, 1, 0, 1)
    SearchingWidget.lineEdit.returnPressed.connect(self.searchWithEnter)
    SearchingWidget.lineEdit.textChanged.connect(self.searchTextChanged)
    self.showErrorMessage = False

    SearchingWidget.completer = QCompleter(SearchingWidget.dictionaryWords)
    SearchingWidget.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    SearchingWidget.completer.activated.connect(self.searchWithClick)
    SearchingWidget.completer.popup().setFont(completerFont)
    SearchingWidget.lineEdit.setCompleter(SearchingWidget.completer)
    SearchingWidget.lineEdit.setPlaceholderText("Please enter a word.")

    self.searchBarWidget = QWidget()
    self.searchBarWidget.layout = QHBoxLayout(self.searchBarWidget)
    self.searchBarWidget.layout.setContentsMargins(10, 0, 0, 0)

    self.clearSearchButton = QPushButton()
    self.clearSearchButton.setIcon(QIcon("Resources/clearSearch.png"))
    self.clearSearchButton.setFixedWidth(30)
    self.clearSearchButton.clicked.connect(self.clearSearch)
    self.hideClearSearchButton = True
    self.clearSearchButton.hide()

    self.searchButton = QPushButton()
    self.searchButton.setIcon(QIcon("Resources/search.png"))
    self.searchButton.setFixedWidth(30)
    self.searchButton.clicked.connect(self.searchWithEnter)

    self.searchBarWidget.layout.setSpacing(0)
    self.searchBarWidget.layout.addWidget(self.lineEdit)
    self.searchBarWidget.layout.addWidget(self.clearSearchButton)
    self.searchBarWidget.layout.addWidget(self.searchButton)
    self.searchBarWidget.layout.addSpacing(5)

    SearchingWidget.errorMessage = QLabel(SearchingWidget.uninitializedStateText, self)
    SearchingWidget.errorMessage.setFont(errorMessageFont)
    sizePolicy = SearchingWidget.errorMessage.sizePolicy()
    sizePolicy.setRetainSizeWhenHidden(True)
    SearchingWidget.errorMessage.setSizePolicy(sizePolicy)
    SearchingWidget.errorMessage.hide()
    SearchingWidget.errorMessage.setStyleSheet(
      "QLabel { color: red }\n"
      "QLabel { background-color: none }\n"
      "QLabel { border: none }\n"
      "QLabel { margin-left: 2px }"
    )

    editWordsButtonFont = QFont(Settings.font, 14)
    self.editWordsButton = QPushButton("Edit Dictionary Words")
    self.editWordsButton.setFont(editWordsButtonFont)
    self.editWordsButton.setContentsMargins(0, 0, 0, 0)
    self.editWordsButton.clicked.connect(self.openWordsEditingWidget)
    self.editWordsButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

    self.subwidget = QWidget()
    self.subwidget.layout = QHBoxLayout(self.subwidget)
    self.subwidget.layout.addWidget(SearchingWidget.errorMessage)
    self.subwidget.layout.addWidget(self.editWordsButton)

    self.layout.addWidget(self.searchBarWidget)
    self.layout.addWidget(self.subwidget)

    self.searchBarFocusShortcut = QShortcut(QKeySequence('/'), self)
    self.searchBarFocusShortcut.activated.connect(SearchingWidget.setFocusToSearchBar)

    self.style()
    self.setFocusedStyleSheet()

  def style(self):
    SearchingWidget.lineEdit.setStyleSheet(
      "QLineEdit { color: blue }"
    )

    self.subwidget.setStyleSheet("""
      QPushButton { border: 1px solid black; border-radius: 10px; padding: 5px 50px }
      QPushButton:hover { background-color: grey }
      """
    )

  def setFocusedStyleSheet(self):
    self.searchBarWidget.setStyleSheet(Styles.searchingWidgetFocusedStyle)

  def setUnfocusedStyleSheet(self):
    self.searchBarWidget.setStyleSheet(Styles.searchingWidgetUnfocusedStyle)

  def setErrorStyleSheet(self):
    self.searchBarWidget.setStyleSheet(Styles.searchingWidgetErrorStyle)
    SearchingWidget.errorMessage.show()

  @staticmethod
  def modifyErrorMessage():
    SearchingWidget.errorMessage.setText(SearchingWidget.unknownWordMessage())

  @staticmethod
  def unknownWordMessage():
    from MainWidget.currentSearch import CurrentSearch
    return "This word is not contained in the books of " + \
      SearchingWidget.gradesMapping[CurrentSearch.currentGrade] + \
      ". Please search for another word."

  @staticmethod
  def updateDictionaryWords():
    from MainWidget.currentSearch import CurrentSearch
    SearchingWidget.dictionaryWords = DBHandler.getWords(CurrentSearch.currentGrade)
    model = QStringListModel(SearchingWidget.dictionaryWords, SearchingWidget.completer)
    SearchingWidget.completer.setModel(model)

  def searchTextChanged(self):
    if not self.hideClearSearchButton and not SearchingWidget.lineEdit.text():
      self.clearSearchButton.hide()
      self.hideClearSearchButton = True
    elif self.hideClearSearchButton and SearchingWidget.lineEdit.text():
      self.clearSearchButton.show()
      self.hideClearSearchButton = False

    if self.showErrorMessage:
      self.showErrorMessage = False
      self.setFocusedStyleSheet()
      SearchingWidget.errorMessage.hide()

  def searchWithEnter(self):
    SearchingWidget.mostRecentlySearchedWord = SearchingWidget.lineEdit.text()

    if SearchingWidget.lineEdit.text() in SearchingWidget.dictionaryWords:
      self.addRecentSearch(SearchingWidget.lineEdit.text())
      self.clearSearch()
    else:
      self.showErrorMessage = True
      self.setErrorStyleSheet()
      SearchingWidget.setFocusToSearchBar()

  def searchWithClick(self, text):
    if not text == SearchingWidget.mostRecentlySearchedWord:
      self.addRecentSearch(text)

    self.clearSearch()

  def clearSearch(self):
    QTimer.singleShot(0, SearchingWidget.lineEdit.clear)
    SearchingWidget.setFocusToSearchBar()

  def addRecentSearch(self, word):
    from MainWidget.mainWidget import MainWidget
    MainWidget.addWord(word)

    recentSearchExists = DBHandler.addRecentSearch(word)
    if recentSearchExists:
      RecentSearchesWidget.removeAndAddRecentSearch(word)
    else:
      RecentSearchesWidget.addRecentSearch(word, False)

  @staticmethod
  def setFocusToSearchBar():
    SearchingWidget.lineEdit.setFocus()

  def openWordsEditingWidget(self):
    settingsDialog = WordsEditingWidget()
    settingsDialog.exec()
