from PyQt6.QtWidgets import QLabel, QPushButton, QWidget
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont, QIcon

class Result(QWidget):
  def __init__(self, word):
    super().__init__()

    self.setFixedSize(QSize(300, 200))
    self.word_label = QLabel(self, text=word)
    self.word_label.setGeometry(50, 50, 200, 100)
    self.word_label.setStyleSheet("QLabel {border-radius: 100px \ 50px; border : 2px solid black}")
    # self.word_label.setText("Test")
    self.word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    font = QFont()
    font.setPointSize(20)
    self.word_label.setFont(font)

    self.deleteButton = QPushButton(self)
    self.deleteButton.setGeometry(200, 45, 40, 40)
    self.deleteButton.setStyleSheet(
      "QPushButton:hover { background-color: black }\n"
      "QPushButton {border-radius : 20; border : 2px solid black}")
    self.deleteButton.setIcon(QIcon("Resources/delete2.svg"))
    
    # TO-DO
    # self.deleteButton.pressed.connect(self.testing)
    