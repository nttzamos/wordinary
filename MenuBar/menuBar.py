from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget

from MenuBar.settings import Settings
from MenuBar.settingsWidget import SettingsWidget

class MenuBar(QWidget):
  def __init__(self, parent):
    super().__init__()
    self.parent = parent

    self.layout = QHBoxLayout(self)
    self.layout.setSpacing(0)
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.setMaximumHeight(30)

    self.applicationIcon = QPushButton()
    self.applicationIcon.setIcon(QIcon("Resources/windowIcon.svg"))
    self.applicationIcon.setFixedHeight(30)
    self.applicationIcon.setFixedWidth(30)

    self.title = QLabel("My Dissertation Title")
    font = QFont(Settings.font, 14)
    self.title.setFont(font)

    self.settingsButton = QPushButton()
    self.settingsButton.setIcon(QIcon("Resources/settings.png"))
    self.settingsButton.setFixedHeight(30)
    self.settingsButton.setFixedWidth(30)
    self.settingsButton.clicked.connect(self.openSettings)

    self.minimizeWindowButton = QPushButton()
    self.minimizeWindowButton.setIcon(QIcon("Resources/minimizeWindow.png"))
    self.minimizeWindowButton.setFixedHeight(30)
    self.minimizeWindowButton.setFixedWidth(30)
    self.minimizeWindowButton.clicked.connect(self.minimizeWindow)

    self.restoreDownWindowButton = QPushButton()
    self.restoreDownWindowButton.setIcon(QIcon("Resources/restoreDownWindow.png"))
    self.restoreDownWindowButton.setFixedHeight(30)
    self.restoreDownWindowButton.setFixedWidth(30)
    self.restoreDownWindowButton.clicked.connect(self.restoreDownWindow)

    self.closeWindowButton = QPushButton()
    self.closeWindowButton.setIcon(QIcon("Resources/closeWindow.png"))
    self.closeWindowButton.setFixedHeight(30)
    self.closeWindowButton.setFixedWidth(30)
    self.closeWindowButton.clicked.connect(self.closeWindow)

    self.layout.addWidget(self.applicationIcon)
    self.layout.addSpacing(5)
    self.layout.addWidget(self.title)
    self.layout.addWidget(self.settingsButton, alignment=Qt.AlignmentFlag.AlignTop)
    self.layout.addWidget(self.minimizeWindowButton, alignment=Qt.AlignmentFlag.AlignTop)
    self.layout.addWidget(self.restoreDownWindowButton, alignment=Qt.AlignmentFlag.AlignTop)
    self.layout.addWidget(self.closeWindowButton, alignment=Qt.AlignmentFlag.AlignTop)

    self.style()

  def style(self):
    from Common.styles import Styles
    self.setStyleSheet(Styles.menuBarStyle)
    self.applicationIcon.setStyleSheet(Styles.applicationIconStyle)
    self.closeWindowButton.setStyleSheet(Styles.closeWindowButtonStyle)

  def openSettings(self):
    settingsDialog = SettingsWidget()
    settingsDialog.exec()

  def minimizeWindow(self):
    self.parent.showMinimized()

  def restoreDownWindow(self):
    pass

  def maximizeWindow(self):
    pass

  def closeWindow(self):
    self.parent.close()