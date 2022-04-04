from PyQt6.QtWidgets import (QGridLayout, QVBoxLayout, QHBoxLayout, QWidget,
                             QLineEdit, QLabel, QGroupBox, QScrollArea,
                             QCheckBox, QPushButton, QMessageBox, QSizePolicy)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

from menu.settings import Settings
from models.profile import get_profiles
from models.student import create_student, student_name_exists

import gettext

language_code = Settings.get_setting('language')
language = gettext.translation('dialogs', localedir='resources/locale', languages=[language_code])
language.install()
_ = language.gettext

class StudentAdditionWidget(QWidget):
  MAXIMUM_NAME_LENGTH = 20

  def __init__(self):
    super().__init__()

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(20, 0, 20, 10)
    self.layout.setSpacing(0)

    StudentAdditionWidget.last_index_used = -1

    section_label_font = QFont(Settings.FONT, 16)
    check_box_font = QFont(Settings.FONT, 14)
    line_edit_font = QFont(Settings.FONT, 14)
    label_font = QFont(Settings.FONT, 12)

    self.success_label = QLabel(_('SUCCESS_SAVING_STUDENT_TEXT'))
    self.success_label.setFont(label_font)
    size_policy = self.success_label.sizePolicy()
    size_policy.setRetainSizeWhenHidden(True)
    self.success_label.setSizePolicy(size_policy)
    self.success_label.hide()
    self.success_label.setStyleSheet('QLabel { color: green }')

    name_widget = QGroupBox(_('STUDENT_NAME_TEXT'))
    name_widget.setFont(section_label_font)
    name_widget.layout = QHBoxLayout(name_widget)
    name_widget.layout.setContentsMargins(10, 5, 10, 10)

    self.name_line_edit = QLineEdit()
    self.name_line_edit.setFont(line_edit_font)
    name_widget.layout.addWidget(self.name_line_edit)

    profiles_widget = QGroupBox(_('PROFILE_SELECTION_TEXT'))
    profiles_widget.setFont(section_label_font)
    profiles_widget.layout = QHBoxLayout(profiles_widget)
    profiles_widget.layout.setContentsMargins(10, 5, 10, 10)

    StudentAdditionWidget.profiles_selection_widget = QWidget()
    StudentAdditionWidget.profiles_selection_widget.layout = \
      QGridLayout(StudentAdditionWidget.profiles_selection_widget)

    StudentAdditionWidget.profiles_selection_widget.setSizePolicy(
      QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum
    )

    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setWidget(StudentAdditionWidget.profiles_selection_widget)
    scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

    profiles = get_profiles()

    StudentAdditionWidget.check_boxes = []
    for i in range(len(profiles)):
      check_box = QCheckBox(profiles[i])
      check_box.setFont(check_box_font)
      StudentAdditionWidget.check_boxes.append(check_box)
      StudentAdditionWidget.profiles_selection_widget.layout.addWidget(check_box, i, 0)
      StudentAdditionWidget.last_index_used = i

    vspacer = QLabel('f')
    invisible_font = QFont(Settings.FONT, 1)
    vspacer.setFont(invisible_font)
    size_policy = vspacer.sizePolicy()
    size_policy.setRetainSizeWhenHidden(True)
    vspacer.setSizePolicy(size_policy)
    StudentAdditionWidget.profiles_selection_widget.layout.addWidget(vspacer, 1000, 0)

    profiles_widget.layout.addWidget(scroll_area)

    save_button = QPushButton(_('SAVE_STUDENT_BUTTON_TEXT'))
    save_button.pressed.connect(self.save_student)
    save_button.setAutoDefault(False)

    select_all_button = QPushButton(_('SELECT_ALL_PROFILES_TEXT'))
    select_all_button.pressed.connect(self.select_all)
    select_all_button.setAutoDefault(False)

    buttons_widget = QWidget()
    buttons_widget.layout = QHBoxLayout(buttons_widget)
    buttons_widget.layout.addWidget(select_all_button, alignment=Qt.AlignmentFlag.AlignLeft)
    buttons_widget.layout.addWidget(save_button, alignment=Qt.AlignmentFlag.AlignRight)

    self.layout.addWidget(self.success_label, alignment=Qt.AlignmentFlag.AlignRight)
    self.layout.addWidget(name_widget)
    self.layout.addWidget(profiles_widget)
    self.layout.addSpacing(10)
    self.layout.addWidget(buttons_widget)

  def save_student(self):
    is_invalid, text = self.student_is_invalid()

    if is_invalid:
      title = _('ERROR_SAVING_STUDENT_TEXT')
      QMessageBox.critical(self, title, text, QMessageBox.StandardButton.Ok)
      return

    student_name = self.name_line_edit.text()
    QTimer.singleShot(0, self.name_line_edit.clear)

    checked_profiles = []
    for check_box in StudentAdditionWidget.check_boxes:
      if check_box.isChecked():
        checked_profiles.append(check_box.text())
        check_box.setChecked(False)

    create_student(student_name, checked_profiles)

    from dialogs.student_update_widget import StudentUpdateWidget
    StudentUpdateWidget.add_student(student_name)

    from search.current_search import CurrentSearch
    CurrentSearch.add_student(student_name)

    self.success_label.show()
    QTimer.singleShot(3500, self.success_label.hide)

  def select_all(self):
    for check_box in StudentAdditionWidget.check_boxes:
      check_box.setChecked(True)

  def student_is_invalid(self):
    student_name = self.name_line_edit.text()
    if len(student_name) == 0:
      return True, _('STUDENT_NAME_EMPTY_TEXT')

    if len(student_name) > StudentAdditionWidget.MAXIMUM_NAME_LENGTH:
      return True, _('STUDENT_NAME_LENGTH_EXCEEDS_LIMIT_TEXT')

    if student_name_exists(student_name):
      return True, _('STUDENT_NAME_EXISTS_TEXT')

    for check_box in StudentAdditionWidget.check_boxes:
      if check_box.isChecked():
        return False, ''

    return True, _('NO_PROFILE_SELECTED_TEXT')

  @staticmethod
  def add_profile(profile_name):
    check_box = QCheckBox(profile_name)
    check_box_font = QFont(Settings.FONT, 14)
    check_box.setFont(check_box_font)
    StudentAdditionWidget.check_boxes.append(check_box)
    StudentAdditionWidget.last_index_used += 1
    StudentAdditionWidget.profiles_selection_widget.layout.addWidget(
      check_box, StudentAdditionWidget.last_index_used, 0
    )

  @staticmethod
  def update_profile(old_profile_name, new_profile_name):
    for check_box in StudentAdditionWidget.check_boxes:
      if check_box.text() == old_profile_name:
        check_box.setText(new_profile_name)
        return

  @staticmethod
  def remove_profile(profile_name):
    for check_box in StudentAdditionWidget.check_boxes:
      if check_box.text() == profile_name:
        StudentAdditionWidget.profiles_selection_widget.layout.removeWidget(check_box)
        StudentAdditionWidget.check_boxes.remove(check_box)
        return
