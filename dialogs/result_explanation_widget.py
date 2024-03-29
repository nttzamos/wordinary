from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QGroupBox, QPushButton)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from menu.settings import Settings
from shared.font_settings import FontSettings

import gettext

class ResultExplanationWidget(QDialog):
  def __init__(self):
    super().__init__()

    language_code = Settings.get_setting('language')
    language = gettext.translation('dialogs', localedir='resources/locale', languages=[language_code])
    language.install()
    _ = language.gettext

    self.setWindowTitle(_('RESULT_EXPLANATION_DIALOG_TITLE'))
    self.setWindowIcon(QIcon('resources/window_icon.png'))
    self.setFixedHeight(450)
    self.setFixedWidth(800)

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(20, 10, 20, 10)
    self.layout.setSpacing(10)

    section_label_font = FontSettings.get_font('heading')
    text_font = FontSettings.get_font('text')
    button_font = FontSettings.get_font('button')

    group_box_widget = QGroupBox(_('RESULT_EXPLANATION_TITLE'))
    group_box_widget.setFont(section_label_font)
    group_box_widget.layout = QHBoxLayout(group_box_widget)
    group_box_widget.layout.setContentsMargins(0, 0, 0, 0)

    explanation = QLabel(_('RESULT_EXPLANATION_TEXT'))
    explanation.setWordWrap(True)
    explanation.setFont(text_font)

    group_box_widget.layout.addWidget(explanation, alignment=Qt.AlignmentFlag.AlignTop)

    self.close_tutorial_button = QPushButton(_('CLOSE_BUTTON_TEXT'))
    self.close_tutorial_button.setFont(button_font)
    self.close_tutorial_button.adjustSize()
    self.close_tutorial_button.pressed.connect(self.close)
    self.close_tutorial_button.setAutoDefault(False)

    self.layout.addWidget(group_box_widget)
    self.layout.addWidget(self.close_tutorial_button, alignment=Qt.AlignmentFlag.AlignRight)

    self.style()

  def style(self):
    from shared.styles import Styles
    self.setStyleSheet(Styles.tutorial_widget_style)
    self.close_tutorial_button.setStyleSheet(Styles.dialog_button_style)
