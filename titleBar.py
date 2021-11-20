from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget

class TitleBar(QWidget):
  title = "My Dissertation Title"

  def __init__(self, parent):
    super().__init__()
    self.parent = parent

    self.layout = QHBoxLayout(self)
    self.layout.setSpacing(0)
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.setFixedHeight(30)

    self.setStyleSheet(
      "QPushButton:hover { background-color: grey; }\n"
      "QPushButton { border: none; }\n"
      "QPushButton { padding-bottom: 5; }\n"
      "QPushButton { padding-top: 5}")

    self.title = QLabel(TitleBar.title)
    font = QFont()
    font.setPointSize(14)
    self.title.setFont(font)

    # self.windowIcon = QIcon("Resources/windowIcon.svg")

    self.settingsButton = QPushButton()
    self.settingsButton.setIcon(QIcon("Resources/settings.png"))
    self.settingsButton.setFixedWidth(30)
    self.settingsButton.clicked.connect(self.openSettings)

    self.minimizeWindowButton = QPushButton()
    self.minimizeWindowButton.setIcon(QIcon("Resources/minimizeWindow.png"))
    self.minimizeWindowButton.setFixedWidth(30)
    self.minimizeWindowButton.clicked.connect(self.minimizeWindow)

    self.restoreDownWindowButton = QPushButton()
    self.restoreDownWindowButton.setIcon(QIcon("Resources/restoreDownWindow.png"))
    self.restoreDownWindowButton.setFixedWidth(30)
    self.restoreDownWindowButton.clicked.connect(self.restoreDownWindow)
    
    self.closeWindowButton = QPushButton()
    self.closeWindowButton.setIcon(QIcon("Resources/closeWindow.png"))
    self.closeWindowButton.setFixedWidth(30)
    self.closeWindowButton.clicked.connect(self.closeWindow)
    self.closeWindowButton.setStyleSheet(
      "QPushButton:hover { background-color: #D11A2A ; }")

    self.layout.addWidget(self.title)
    # self.layout.addWidget(self.windowIcon)
    self.layout.addWidget(self.settingsButton, alignment=Qt.AlignmentFlag.AlignTop)
    self.layout.addWidget(self.minimizeWindowButton, alignment=Qt.AlignmentFlag.AlignTop)
    self.layout.addWidget(self.restoreDownWindowButton, alignment=Qt.AlignmentFlag.AlignTop)
    self.layout.addWidget(self.closeWindowButton, alignment=Qt.AlignmentFlag.AlignTop)

  def openSettings(self):
    pass
  
  def minimizeWindow(self):
    self.parent.showMinimized()

  def restoreDownWindow(self):
    pass

  def maximizeWindow(self):
    pass

  def closeWindow(self):
    self.parent.close()