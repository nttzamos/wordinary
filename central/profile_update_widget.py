from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QLabel, QGroupBox, QScrollArea, QCheckBox, QPushButton, QComboBox, QSizePolicy, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from shared.database_handler import get_grades, get_grade_subjects
from menu.settings import Settings

from models.profile import *

class ProfileUpdateWidget(QWidget):
  def __init__(self):
    super().__init__()

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(20, 10, 20, 10)
    self.layout.setSpacing(0)

    section_label_font = QFont(Settings.font, 16)
    combo_box_font = QFont(Settings.font, 14)
    label_font = QFont(Settings.font, 14)
    line_edit_font = QFont(Settings.font, 14)

    profile_selection_widget = QGroupBox('Profile Selection')
    profile_selection_widget.setFont(section_label_font)
    profile_selection_widget.layout = QHBoxLayout(profile_selection_widget)
    profile_selection_widget.layout.setContentsMargins(10, 5, 10, 10)

    profiles = get_profiles()

    ProfileUpdateWidget.profile_selector = QComboBox()
    ProfileUpdateWidget.profile_selector.setFont(combo_box_font)

    if len(profiles) == 0:
      ProfileUpdateWidget.profile_selector.addItem('There are no profiles')
      ProfileUpdateWidget.profile_selector.setDisabled(True)
    else:
      profiles[0:0] = ['Please select a profile...']
      ProfileUpdateWidget.profile_selector.addItems(profiles)

    ProfileUpdateWidget.profile_selector.activated.connect(self.profile_selector_activated_initial)

    profile_selection_widget.layout.addWidget(ProfileUpdateWidget.profile_selector)

    self.name_widget = QGroupBox('Profile Name')
    self.name_widget.setFont(section_label_font)
    self.name_widget.layout = QHBoxLayout(self.name_widget)
    self.name_widget.layout.setContentsMargins(10, 5, 10, 10)

    self.name_line_edit = QLineEdit()
    self.name_line_edit.setFont(line_edit_font)
    self.name_widget.layout.addWidget(self.name_line_edit)
    self.name_widget.hide()

    grade_label_widget = QGroupBox('Profile Grade')
    grade_label_widget.setFont(section_label_font)
    grade_label_widget.layout = QHBoxLayout(grade_label_widget)
    grade_label_widget.layout.setContentsMargins(10, 5, 10, 10)

    ProfileUpdateWidget.grade_label = QLabel('Please select a profile...')
    ProfileUpdateWidget.grade_label.setFont(label_font)

    grade_label_widget.layout.addWidget(ProfileUpdateWidget.grade_label)

    subjects_widget = QGroupBox('Subject Selection')
    subjects_widget.setFont(section_label_font)
    subjects_widget.layout = QHBoxLayout(subjects_widget)
    subjects_widget.layout.setContentsMargins(10, 5, 10, 10)

    self.subjects_selection_widget = QWidget()
    self.subjects_selection_widget.layout = QGridLayout(self.subjects_selection_widget)
    self.subjects_selection_widget.setDisabled(True)

    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setWidget(self.subjects_selection_widget)
    scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
    self.subjects_selection_widget.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

    self.check_boxes = []

    vspacer = QLabel('f')
    invisible_font = QFont(Settings.font, 1)
    vspacer.setFont(invisible_font)
    size_policy = vspacer.sizePolicy()
    size_policy.setRetainSizeWhenHidden(True)
    vspacer.setSizePolicy(size_policy)
    self.subjects_selection_widget.layout.addWidget(vspacer, 1000, 0)

    subjects_widget.layout.addWidget(scroll_area)

    self.save_button = QPushButton('Update Existing Profile')
    self.save_button.pressed.connect(self.update_profile)
    self.save_button.setDisabled(True)

    self.delete_button = QPushButton('Delete Profile')
    self.delete_button.pressed.connect(self.delete_profile)
    self.delete_button.setDisabled(True)

    buttons_widget = QWidget()
    buttons_widget.layout = QHBoxLayout(buttons_widget)
    buttons_widget.layout.setContentsMargins(0, 0, 0, 0)
    buttons_widget.layout.addWidget(self.delete_button)
    buttons_widget.layout.addSpacing(10)
    buttons_widget.layout.addWidget(self.save_button)

    self.layout.addWidget(profile_selection_widget)
    self.layout.addWidget(self.name_widget)
    self.layout.addWidget(grade_label_widget)
    self.layout.addWidget(subjects_widget)
    self.layout.addSpacing(15)
    self.layout.addWidget(buttons_widget, alignment=Qt.AlignmentFlag.AlignRight)

    self.style()

  def style(self):
    from shared.styles import Styles
    self.setStyleSheet(Styles.profile_update_style)

  def profile_selector_activated_initial(self, index):
    if index != 0:
      ProfileUpdateWidget.profile_selector.removeItem(0)
      ProfileUpdateWidget.profile_selector.activated.disconnect()
      ProfileUpdateWidget.profile_selector.activated.connect(self.profile_selector_activated)
      self.profile_selector_activated(index - 1)
      self.save_button.setEnabled(True)
      self.delete_button.setEnabled(True)
      self.subjects_selection_widget.setEnabled(True)
      self.name_widget.show()

  def profile_selector_activated(self, index):
    profile_name = ProfileUpdateWidget.profile_selector.currentText()
    self.profile_id, self.grade_id, grade_name, self.profile_subjects = get_profile_details(profile_name)
    ProfileUpdateWidget.grade_label.setText(grade_name)
    self.name_line_edit.setText(profile_name)
    grade_subjects = get_grade_subjects(self.grade_id)

    for check_box in self.check_boxes:
      self.subjects_selection_widget.layout.removeWidget(check_box)

    check_box_font = QFont(Settings.font, 14)
    self.check_boxes = []
    for i in range(len(grade_subjects)):
      check_box = QCheckBox(grade_subjects[i])
      check_box.setFont(check_box_font)
      self.check_boxes.append(check_box)

      if grade_subjects[i] in self.profile_subjects:
        check_box.setChecked(True)

      self.subjects_selection_widget.layout.addWidget(check_box, i, 0)

  def update_profile(self):
    if self.profile_selector.currentText() in get_grades():
      is_invalid, text = True, 'Grade profiles can not be updated.'
    else:
      is_invalid, text = self.profile_is_invalid()

    if is_invalid:
      title = 'Error Updating Profile'
      answer = QMessageBox.critical(self, title, text, QMessageBox.StandardButton.Ok)
      if answer == QMessageBox.StandardButton.Ok:
        return

    old_profile_name = ProfileUpdateWidget.profile_selector.currentText()
    new_profile_name = self.name_line_edit.text()

    from central.current_search import CurrentSearch
    CurrentSearch.update_profile(old_profile_name, new_profile_name)

    from central.student_addition_widget import StudentAdditionWidget
    StudentAdditionWidget.update_profile(old_profile_name, new_profile_name)

    from central.student_update_widget import StudentUpdateWidget
    StudentUpdateWidget.update_profile(old_profile_name, new_profile_name)

    self.profile_selector.setItemText(self.profile_selector.currentIndex(), new_profile_name)
    update_profile_name(self.profile_id, new_profile_name)

    subjects_names = []
    for check_box in self.check_boxes:
      if check_box.isChecked():
        subjects_names.append(check_box.text())

    subjects_to_remove = list(set(self.profile_subjects) - set(subjects_names))
    subjects_to_add = list(set(subjects_names) - set(self.profile_subjects))
    self.profile_subjects = subjects_names
    add_profile_subjects(self.grade_id, self.profile_id, subjects_to_add)
    remove_profile_subjects(self.grade_id, self.profile_id, subjects_to_remove)

    if CurrentSearch.profile_selector.currentText() == new_profile_name:
      CurrentSearch.add_subjects(subjects_to_add)
      CurrentSearch.remove_subjects(subjects_to_remove)

  def delete_profile(self):
    if self.profile_selector.currentText() in get_grades():
      title = 'Error Deleting Profile'
      text = 'Grade profiles can not be deleted.'
      answer = QMessageBox.critical(self, title, text, QMessageBox.StandardButton.Ok)
      if answer == QMessageBox.StandardButton.Ok:
        return

    destroy_profile(self.profile_id)
    for check_box in self.check_boxes:
      self.subjects_selection_widget.layout.removeWidget(check_box)

    from central.student_addition_widget import StudentAdditionWidget
    StudentAdditionWidget.remove_profile(ProfileUpdateWidget.profile_selector.currentText())

    from central.student_update_widget import StudentUpdateWidget
    StudentUpdateWidget.remove_profile(ProfileUpdateWidget.profile_selector.currentText())

    from central.current_search import CurrentSearch
    CurrentSearch.remove_profiles([ProfileUpdateWidget.profile_selector.currentText()])

    ProfileUpdateWidget.profile_selector.removeItem(ProfileUpdateWidget.profile_selector.currentIndex())
    if ProfileUpdateWidget.profile_selector.count() == 0:
      ProfileUpdateWidget.profile_selector.addItem('There are no profiles')
      ProfileUpdateWidget.profile_selector.setDisabled(True)
      ProfileUpdateWidget.profile_selector.activated.disconnect()
      ProfileUpdateWidget.profile_selector.activated.connect(self.profile_selector_activated_initial)
      ProfileUpdateWidget.grade_label.setText('You have to add a profile...')
      self.name_widget.hide()
      return

    self.profile_selector_activated(0)

  def profile_is_invalid(self):
    profile_name = self.name_line_edit.text()
    if len(profile_name) == 0:
      return True, 'Profile can not be updated because the profile name is empty.'

    if ProfileUpdateWidget.profile_selector.currentText() != profile_name and profile_name_exists(profile_name):
      return True, 'Profile can not be updated as this name is already used for another profile.'

    for check_box in self.check_boxes:
      if check_box.isChecked():
        return False, ''

    return True, 'Profile can not be updated because none of the grade subjects have been selected.'

  @staticmethod
  def add_profile(profile_name):
    if ProfileUpdateWidget.profile_selector.currentText() == 'There are no profiles':
      ProfileUpdateWidget.profile_selector.setItemText(0, 'Please select a profile...')
      ProfileUpdateWidget.grade_label.setText('Please select a profile...')
      ProfileUpdateWidget.profile_selector.setEnabled(True)

    ProfileUpdateWidget.profile_selector.addItem(profile_name)