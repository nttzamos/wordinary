from PyQt6.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont, QIcon

class Result(QWidget):
  def __init__(self, word):
    super().__init__()

    self.layout = QHBoxLayout(self)
    self.layout.setContentsMargins(0, 0, 10, 10)

    dataWidget = QWidget()
    dataWidget.layout = QVBoxLayout(dataWidget)
    dataWidget.layout.setContentsMargins(0, 25, 0, 25)

    # Word
    self.word_label = QLabel(self, text=word)
    self.word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    from settings import Settings
    font = QFont(Settings.font, 20)
    self.word_label.setFont(font)

    # Buttons
    self.buttonsWidget = QWidget()
    self.buttonsWidget.layout = QHBoxLayout(self.buttonsWidget)
    self.buttonsWidget.layout.setContentsMargins(0, 0, 0, 0)

    self.searchButton = QPushButton()
    self.searchButton.setIcon(QIcon("Resources/reload.svg"))
    self.searchButton.clicked.connect(self.searchWord)
    self.searchButton.setFixedWidth(30)

    self.starButton = QPushButton()
    self.starButton.clicked.connect(self.starWord)
    self.starButton.setFixedWidth(30)
    self.starButton.setIcon(QIcon("Resources/starred.svg"))

    self.buttonsWidget.layout.addWidget(self.searchButton)
    self.buttonsWidget.layout.addWidget(self.starButton)

    dataWidget.layout.addWidget(self.word_label)
    dataWidget.layout.addWidget(self.buttonsWidget)
    
    self.layout.addWidget(dataWidget)

    self.style()

  def style(self):
    self.setStyleSheet(
      "QWidget { background-color: white; border-radius: 10px}\n"
      "QPushButton { background-color: white }\n"
      "QPushButton:hover { background-color: grey }\n"
      "QPushButton { border-radius: 12px }\n"
      "QPushButton { border: 1px solid black }\n"
      "QPushButton { padding-bottom: 5px }\n"
      "QPushButton { padding-top: 5px }\n"
      "QLabel { color: blue }"
    )

  def searchWord(self):
    pass

  def starWord(self):
    pass
