from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QLabel, QGroupBox, QScrollArea, QCheckBox, QPushButton, QMessageBox
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

from menu.settings import Settings

from models.student import create_student, student_name_exists
from models.profile import get_profiles

class StudentAdditionWidget(QWidget):
  last_index_used = -1

  def __init__(self):
    super().__init__()
    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(20, 10, 20, 10)
    self.layout.setSpacing(0)

    section_label_font = QFont(Settings.font, 16)
    check_box_font = QFont(Settings.font, 14)
    line_edit_font = QFont(Settings.font, 14)

    name_widget = QGroupBox('Student Name')
    name_widget.setFont(section_label_font)
    name_widget.layout = QHBoxLayout(name_widget)
    name_widget.layout.setContentsMargins(10, 5, 10, 10)

    self.name_line_edit = QLineEdit()
    self.name_line_edit.setFont(line_edit_font)
    name_widget.layout.addWidget(self.name_line_edit)

    profiles_widget = QGroupBox('Profile Selection')
    profiles_widget.setFont(section_label_font)
    profiles_widget.layout = QHBoxLayout(profiles_widget)
    profiles_widget.layout.setContentsMargins(10, 5, 10, 10)

    StudentAdditionWidget.profiles_selection_widget = QWidget()
    StudentAdditionWidget.profiles_selection_widget.layout = QGridLayout(StudentAdditionWidget.profiles_selection_widget)

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
    invisible_font = QFont(Settings.font, 1)
    vspacer.setFont(invisible_font)
    size_policy = vspacer.sizePolicy()
    size_policy.setRetainSizeWhenHidden(True)
    vspacer.setSizePolicy(size_policy)
    StudentAdditionWidget.profiles_selection_widget.layout.addWidget(vspacer, 1000, 0)

    profiles_widget.layout.addWidget(scroll_area)

    save_button = QPushButton('Save New Student')
    save_button.pressed.connect(self.saveStudent)

    self.layout.addWidget(name_widget)
    self.layout.addWidget(profiles_widget)
    self.layout.addSpacing(15)
    self.layout.addWidget(save_button, alignment=Qt.AlignmentFlag.AlignRight)

    self.style()

  def style(self):
    from shared.styles import Styles
    self.setStyleSheet(Styles.student_addition_style)

  def saveStudent(self):
    is_invalid, text = self.student_is_invalid()

    if is_invalid:
      title = 'Error Saving Student'
      answer = QMessageBox.critical(self, title, text, QMessageBox.StandardButton.Ok)
      if answer == QMessageBox.StandardButton.Ok:
        return

    student_name = self.name_line_edit.text()
    QTimer.singleShot(0, self.name_line_edit.clear)

    checked_profiles = []
    for check_box in StudentAdditionWidget.check_boxes:
      if check_box.isChecked():
        checked_profiles.append(check_box.text())
        check_box.setChecked(False)

    create_student(student_name, checked_profiles)

    from central.student_update_widget import StudentUpdateWidget
    StudentUpdateWidget.add_student(student_name)

    from central.current_search import CurrentSearch
    CurrentSearch.add_student(student_name)

  def student_is_invalid(self):
    student_name = self.name_line_edit.text()
    if len(student_name) == 0:
      return True, 'Student can not be saved because the profile name is empty.'

    if student_name_exists(student_name):
      return True, 'Student can not be saved as this name is already used for another profile.'

    for check_box in StudentAdditionWidget.check_boxes:
      if check_box.isChecked():
        return False, ''

    return True, 'Student can not be saved because none of the profiles have been selected.'

  @staticmethod
  def add_profile(profile_name):
    check_box = QCheckBox(profile_name)
    check_box_font = QFont(Settings.font, 14)
    check_box.setFont(check_box_font)
    StudentAdditionWidget.check_boxes.append(check_box)
    StudentAdditionWidget.last_index_used += 1
    StudentAdditionWidget.profiles_selection_widget.layout.addWidget(check_box, StudentAdditionWidget.last_index_used, 0)

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