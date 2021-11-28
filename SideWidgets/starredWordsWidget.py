from PyQt6.QtWidgets import QGridLayout, QLabel, QScrollArea, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ItemWidgets.starredWord import StarredWord
from databaseHandler import DBHandler
from settings import Settings

class StarredWordsWidget(QWidget):
  title = "Starred Words"

  scrollAreaWidgetContents = QWidget()
  gridLayout = QGridLayout(scrollAreaWidgetContents)
  gridLayout.setSpacing(0)
  gridLayout.setContentsMargins(0, 0, 0, 0)
  
  counter = 1000000
  widgetList = []
  
  placeholderLabel = QLabel("You do not have any " + title)
  placeholderLabelShow = False

  def __init__(self):
    super().__init__()

    self.layout = QVBoxLayout(self)
    self.titleLabel = QLabel(StarredWordsWidget.title)
    self.titleLabel.setStyleSheet("QLabel {border : 1px solid black; padding: 10px 0px}")
    self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
    font = QFont(Settings.font, 18)
    self.titleLabel.setFont(font)
    self.layout.addWidget(self.titleLabel)
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.layout.setSpacing(0)

    StarredWordsWidget.placeholderLabel.setFont(font)
    self.scrollArea = QScrollArea()
    self.scrollArea.setWidgetResizable(True)
    self.scrollArea.setWidget(StarredWordsWidget.scrollAreaWidgetContents)
    self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
    self.layout.addWidget(self.scrollArea)

    self.vspacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
    StarredWordsWidget.gridLayout.addItem(self.vspacer, 2000000, 0, 1, -1)

    self.setFixedWidth(self.getMaximumWidth())
    
  def initialize(self, starredWordsList):
    for word in starredWordsList:
      widget = StarredWord(word)
      StarredWordsWidget.widgetList.append(widget)
      StarredWordsWidget.gridLayout.addWidget(widget, StarredWordsWidget.counter, 0)
      StarredWordsWidget.counter -= 1

  def getMaximumWidth(self):
    longStarredWord = StarredWord("0123456789012345678901234")
    return longStarredWord.sizeHint().width()

  @staticmethod
  def addStarredWord(word):
    if StarredWordsWidget.placeholderLabelShow == True:
      StarredWordsWidget.placeholderLabel.hide()
      
    widget = StarredWord(word)
    StarredWordsWidget.widgetList.append(widget)
    length = len(StarredWordsWidget.widgetList)
    StarredWordsWidget.gridLayout.addWidget(StarredWordsWidget.widgetList[length-1], StarredWordsWidget.counter, 0)
    StarredWordsWidget.counter -= 1

  @staticmethod
  def removeStarredWord(obj):
    StarredWordsWidget.widgetList.remove(obj)
    if len(StarredWordsWidget.widgetList)==0:
      StarredWordsWidget.addPlaceholder()

  @staticmethod
  def toggleStarredBottom(word):
    for obj in StarredWordsWidget.widgetList:
      if word==obj.word.text():
        obj.removeWord()
        return

  @staticmethod
  def addPlaceholder():
    StarredWordsWidget.placeholderLabelShow = True
    StarredWordsWidget.gridLayout.addWidget(StarredWordsWidget.placeholderLabel)
    StarredWordsWidget.placeholderLabel.show()
