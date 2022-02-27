from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QDialog, QCheckBox, QRadioButton, QSpinBox, QLabel, QGroupBox, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont

from menu.settings import Settings

import os
import shutil

class SettingsWidget(QDialog):
  TITLE_TEXT = 'Ρυθμίσεις'
  RESULTS_TEXT = 'Αριθμός Αποτελεσμάτων'
  MAXIMUM_RESULTS_TEXT = 'Μέγιστος αριθμός αποτελεσμάτων'
  GENERAL_SETTINGS_TEXT = 'Γενικές Ρυθμίσεις'
  REMEMBER_LAST_STUDENT_TEXT = 'Αυτόματη επιλογή του τελευτ'
  ASK_BEFORE_ACTION_TEXT = 'ερερ'
  SHOW_EDIT_WORDS_BUTTON_TEXT = 'Εμφάνιση επιλογής επεξεργασίας λέξεων'
  ONLY_SHOW_WORDS_WITH_FAMILY_TEXT = 'Εμφάνιση μόνο λέξεων '
  THEME_SELECTION_TEXT = 'Επιλογή Θέματος'
  LIGHT_THEME_TEXT = 'Ανοιχτό'
  DARK_THEME_TEXT = 'Σκοτεινό'
  RESTORE_TEXT = 'Επαναφορά Δεδομένων'
  RESTORE_DATABASE_TEXT = 'Διαγραφή δεδομένων χρήστη'
  SHOW_TUTORIAL_TEXT = 'Εμφανισή οδηγιών κατά την εκκίνηση'

  def __init__(self):
    super().__init__()
    self.setWindowTitle(SettingsWidget.TITLE_TEXT)
    self.setWindowIcon(QIcon('resources/window_icon.png'))

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(20, 20, 20, 20)
    self.layout.setSpacing(20)

    section_label_font = QFont(Settings.font, 16)
    spin_box_font = QFont(Settings.font, 12)

    maximum_results_label = QLabel(SettingsWidget.MAXIMUM_RESULTS_TEXT)
    self.maximum_results_spin_box = QSpinBox()
    self.maximum_results_spin_box.setFont(spin_box_font)
    self.maximum_results_spin_box.valueChanged.connect(self.maximum_results_changed)
    self.maximum_results_spin_box.setValue(Settings.get_setting('maximum_results'))
    self.maximum_results_spin_box.setMinimum(1)
    self.maximum_results_spin_box.setMaximum(50)

    maximum_results_selection_widget = QGroupBox(SettingsWidget.RESULTS_TEXT)
    maximum_results_selection_widget.setFont(section_label_font)
    maximum_results_selection_widget.layout = QHBoxLayout(maximum_results_selection_widget)
    maximum_results_selection_widget.layout.setContentsMargins(10, 0, 0, 0)
    maximum_results_selection_widget.layout.addWidget(maximum_results_label)
    maximum_results_selection_widget.layout.addWidget(self.maximum_results_spin_box)

    general_settings_widget = QGroupBox(SettingsWidget.GENERAL_SETTINGS_TEXT)
    general_settings_widget.setFont(section_label_font)
    general_settings_widget.layout = QVBoxLayout(general_settings_widget)
    general_settings_widget.layout.setContentsMargins(10, 0, 0, 0)

    self.remember_last_student_picked = QCheckBox(SettingsWidget.REMEMBER_LAST_STUDENT_TEXT, objectName='remember_last_student_picked')
    self.remember_last_student_picked.clicked.connect(lambda: self.toggle_setting('remember_last_student_picked'))
    self.remember_last_student_picked.setChecked(Settings.get_boolean_setting('remember_last_student_picked'))

    self.ask_before_actions = QCheckBox(SettingsWidget.ASK_BEFORE_ACTION_TEXT, objectName='ask_before_actions')
    self.ask_before_actions.clicked.connect(lambda: self.toggle_setting('ask_before_actions'))
    self.ask_before_actions.setChecked(Settings.get_boolean_setting('ask_before_actions'))

    self.show_edit_dict_words_button = QCheckBox(SettingsWidget.SHOW_EDIT_WORDS_BUTTON_TEXT, objectName='show_edit_dict_words_button')
    self.show_edit_dict_words_button.clicked.connect(lambda: self.toggle_setting('show_edit_dict_words_button'))
    self.show_edit_dict_words_button.setChecked(Settings.get_boolean_setting('show_edit_dict_words_button'))

    self.only_show_words_with_family = QCheckBox(SettingsWidget.ONLY_SHOW_WORDS_WITH_FAMILY_TEXT, objectName='only_show_words_with_family')
    self.only_show_words_with_family.clicked.connect(lambda: self.toggle_setting('only_show_words_with_family'))
    self.only_show_words_with_family.setChecked(Settings.get_boolean_setting('only_show_words_with_family'))

    self.show_tutorial_on_startup = QCheckBox(SettingsWidget.SHOW_TUTORIAL_TEXT, objectName='show_tutorial_on_startup')
    self.show_tutorial_on_startup.clicked.connect(lambda: self.toggle_setting('show_tutorial_on_startup'))
    self.show_tutorial_on_startup.setChecked(Settings.get_boolean_setting('show_tutorial_on_startup'))

    # general_settings_widget.layout.addWidget(self.remember_last_student_picked)
    # general_settings_widget.layout.addWidget(self.ask_before_actions)
    general_settings_widget.layout.addWidget(self.show_edit_dict_words_button)
    # general_settings_widget.layout.addWidget(self.only_show_words_with_family)
    general_settings_widget.layout.addWidget(self.show_tutorial_on_startup)

    theme_selection_widget = QGroupBox(SettingsWidget.THEME_SELECTION_TEXT)
    theme_selection_widget.setFont(section_label_font)
    theme_selection_widget.layout = QHBoxLayout(theme_selection_widget)
    self.light_theme_button = QRadioButton(SettingsWidget.LIGHT_THEME_TEXT)
    self.light_theme_button.toggled.connect(self.light_theme_button_clicked)
    self.dark_theme_button = QRadioButton(SettingsWidget.DARK_THEME_TEXT)
    self.dark_theme_button.toggled.connect(self.dark_theme_button_clicked)

    if Settings.get_setting('theme') == 'light':
      self.light_theme_button.setChecked(True)
    else:
      self.dark_theme_button.setChecked(True)

    theme_selection_widget.layout.setContentsMargins(10, 0, 0, 0)
    theme_selection_widget.layout.addWidget(self.light_theme_button, alignment=Qt.AlignmentFlag.AlignLeft)
    theme_selection_widget.layout.addWidget(self.dark_theme_button, alignment=Qt.AlignmentFlag.AlignLeft)

    word_family_discovery_widget = QGroupBox('Εύρεση συγγενικών λέξεων')
    word_family_discovery_widget.setFont(section_label_font)
    word_family_discovery_widget.layout = QHBoxLayout(word_family_discovery_widget)
    self.online_wiktionary_button = QRadioButton('Online Wiktionary')
    self.online_wiktionary_button.toggled.connect(self.online_wiktionary_button_clicked)
    self.offline_database_button = QRadioButton('Offline Database')
    self.offline_database_button.toggled.connect(self.offline_database_button_clicked)

    if Settings.get_setting('word_family_discovery') == 'online_wiktionary':
      self.online_wiktionary_button.setChecked(True)
    else:
      self.offline_database_button.setChecked(True)

    word_family_discovery_widget.layout.setContentsMargins(10, 0, 0, 0)
    word_family_discovery_widget.layout.addWidget(self.online_wiktionary_button, alignment=Qt.AlignmentFlag.AlignLeft)
    word_family_discovery_widget.layout.addWidget(self.offline_database_button, alignment=Qt.AlignmentFlag.AlignLeft)

    restore_database_button = QPushButton(SettingsWidget.RESTORE_DATABASE_TEXT)
    restore_database_button.pressed.connect(self.restore_database)
    restore_database_button.setAutoDefault(False)

    restore_database_widget = QGroupBox(SettingsWidget.RESTORE_TEXT)
    restore_database_widget.setFont(section_label_font)
    restore_database_widget.layout = QHBoxLayout(restore_database_widget)
    restore_database_widget.layout.setContentsMargins(50, 10, 50, 10)
    restore_database_widget.layout.addWidget(restore_database_button)

    self.layout.addWidget(maximum_results_selection_widget)
    self.layout.addWidget(general_settings_widget)
    self.layout.addWidget(theme_selection_widget)
    # self.layout.addWidget(word_family_discovery_widget)
    self.layout.addWidget(restore_database_widget)

    self.style()

  def style(self):
    from shared.styles import Styles
    self.setStyleSheet(Styles.settings_widget_style)

  def maximum_results_changed(self):
    Settings.set_setting('maximum_results', self.maximum_results_spin_box.value())

  def toggle_setting(self, setting_name):
    setting_check_box = self.findChild(QCheckBox, setting_name)
    new_value = setting_check_box.isChecked()
    Settings.set_boolean_setting(setting_name, new_value)

    if setting_name == 'show_edit_dict_words_button':
      from search.searching_widget import SearchingWidget
      SearchingWidget.toggle_edit_words_button_visibility(new_value)

    if setting_name == 'only_show_words_with_family':
      from search.searching_widget import SearchingWidget
      SearchingWidget.update_selected_dictionary()

  def light_theme_button_clicked(self):
    if self.light_theme_button.isChecked():
      Settings.set_setting('theme', 'light')

  def dark_theme_button_clicked(self):
    if self.dark_theme_button.isChecked():
      Settings.set_setting('theme', 'dark')

  def online_wiktionary_button_clicked(self):
    if self.online_wiktionary_button.isChecked():
      Settings.set_setting('word_family_discovery', 'online_wiktionary')

  def offline_database_button_clicked(self):
    if self.offline_database_button.isChecked():
      Settings.set_setting('word_family_discovery', 'offline_database')

  def restore_database(self):
    title = 'Επαναφορά Δεδομένων'
    question = ('Είστε σίγουροι ότι θέλετε να επαναφέρετε την βάση δεδομένων '
                'στην αρχική της κατάσταση; Όλα τα δεδομένα σας θα διαγραφούν.')
    answer = QMessageBox.question(self, title, question, QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Yes)
    if answer == QMessageBox.StandardButton.Yes:
      os.remove('resources/database.db')
      shutil.copyfile('resources/database_backup.db', 'resources/database.db')
      from central.main_window import MainWindow
      MainWindow.clear_previous_subject_details()
      from search.current_search import CurrentSearch
      CurrentSearch.clear_current_search_details()
