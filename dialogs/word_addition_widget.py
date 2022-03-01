from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QLabel, QGroupBox, QScrollArea, QCheckBox, QPushButton, QComboBox, QSizePolicy, QMessageBox
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont

from menu.settings import Settings
from models.word import create_word, word_exists
from shared.database_handler import get_grades, get_grade_subjects

class WordAdditionWIdget(QWidget):
  GREEK_CHARACTERS = [
    'α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο',
    'π', 'ρ', 'σ', 'τ', 'υ', 'φ', 'χ', 'ψ', 'ω', 'ς', 'ά', 'έ', 'ί', 'ή', 'ύ', 'ό',
    'ώ', 'ϊ', 'ϋ']

  WORD_TEXT = 'Λέξη'
  GRADE_SELECTION_TEXT = 'Επιλογή Τάξης'
  SUBJECT_SELECTION_TEXT = 'Επιλογή Μαθημάτων'
  SAVE_WORD_BUTTON_TEXT = 'Αποθήκευση λέξης'
  ERROR_SAVING_WORD_TEXT = 'Αδυναμία αποθήκευσης λέξης'
  WORD_EMPTY_TEXT = 'Η λέξη δεν μπορεί να αποθηκευτεί καθώς είναι κενή'
  WORD_EXISTS_TEXT = 'Η λέξη δεν μπορεί να αποθηκευτεί καθώς υπάρχει ήδη'
  ONLY_GREEK_CHARACTERS_ALLOWED_TEXT = 'Η λέξη σας πρέπει να περιέχει μόνο ελληνικούς χαρακτήρες'
  NO_SUBJECT_SELECTED_TEXT = ('Η λέξη δεν μπορεί να αποθηκευτεί καθώς δεν '
                              'έχετε επιλέξει κανένα μάθημα στο οποίο θα ανήκει')

  def __init__(self):
    super().__init__()

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(20, 10, 20, 10)
    self.layout.setSpacing(0)

    section_label_font = QFont(Settings.font, 16)
    combo_box_font = QFont(Settings.font, 14)
    check_box_font = QFont(Settings.font, 14)
    line_edit_font = QFont(Settings.font, 14)

    word_widget = QGroupBox(WordAdditionWIdget.WORD_TEXT)
    word_widget.setFont(section_label_font)
    word_widget.layout = QHBoxLayout(word_widget)
    word_widget.layout.setContentsMargins(10, 5, 10, 10)

    self.word_line_edit = QLineEdit()
    self.word_line_edit.setFont(line_edit_font)
    word_widget.layout.addWidget(self.word_line_edit)

    grade_selection_widget = QGroupBox(WordAdditionWIdget.GRADE_SELECTION_TEXT)
    grade_selection_widget.setFont(section_label_font)
    grade_selection_widget.layout = QHBoxLayout(grade_selection_widget)
    grade_selection_widget.layout.setContentsMargins(10, 5, 10, 10)

    self.grade_selector = QComboBox()
    self.grade_selector.setFont(combo_box_font)
    self.grade_selector.addItems(get_grades())
    self.grade_selector.activated.connect(self.grade_selector_activated)

    grade_selection_widget.layout.addWidget(self.grade_selector)

    subjects_widget = QGroupBox(WordAdditionWIdget.SUBJECT_SELECTION_TEXT)
    subjects_widget.setFont(section_label_font)
    subjects_widget.layout = QHBoxLayout(subjects_widget)
    subjects_widget.layout.setContentsMargins(10, 5, 10, 10)

    self.subjects_selection_widget = QWidget()
    self.subjects_selection_widget.layout = QGridLayout(self.subjects_selection_widget)
    self.subjects_selection_widget.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setWidget(self.subjects_selection_widget)
    scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

    grade_subjects = get_grade_subjects(1)

    self.check_boxes = []
    for i in range(len(grade_subjects)):
      check_box = QCheckBox(grade_subjects[i])
      check_box.setFont(check_box_font)
      self.check_boxes.append(check_box)
      self.subjects_selection_widget.layout.addWidget(check_box, i, 0)

    vspacer = QLabel('f')
    invisible_font = QFont(Settings.font, 1)
    vspacer.setFont(invisible_font)
    size_policy = vspacer.sizePolicy()
    size_policy.setRetainSizeWhenHidden(True)
    vspacer.setSizePolicy(size_policy)
    self.subjects_selection_widget.layout.addWidget(vspacer, 1000, 0)

    subjects_widget.layout.addWidget(scroll_area)

    save_button = QPushButton(WordAdditionWIdget.SAVE_WORD_BUTTON_TEXT)
    save_button.pressed.connect(self.save_word)
    save_button.setAutoDefault(False)

    self.layout.addWidget(word_widget)
    self.layout.addWidget(grade_selection_widget)
    self.layout.addWidget(subjects_widget)
    self.layout.addSpacing(15)
    self.layout.addWidget(save_button, alignment=Qt.AlignmentFlag.AlignRight)

  def grade_selector_activated(self, index):
    for check_box in self.check_boxes:
      self.subjects_selection_widget.layout.removeWidget(check_box)

    grade_subjects = get_grade_subjects(index + 1)

    check_box_font = QFont(Settings.font, 14)
    self.check_boxes = []
    for i in range(len(grade_subjects)):
      check_box = QCheckBox(grade_subjects[i])
      check_box.setFont(check_box_font)
      self.check_boxes.append(check_box)
      self.subjects_selection_widget.layout.addWidget(check_box, i, 0)

  def save_word(self):
    is_invalid, text = self.word_is_invalid()

    if is_invalid:
      title = WordAdditionWIdget.ERROR_SAVING_WORD_TEXT
      answer = QMessageBox.critical(self, title, text, QMessageBox.StandardButton.Ok)
      if answer == QMessageBox.StandardButton.Ok:
        return

    word = self.word_line_edit.text().strip()
    QTimer.singleShot(0, self.word_line_edit.clear)

    subjects = []
    for check_box in self.check_boxes:
      if check_box.isChecked():
        subjects.append(check_box.text())
        check_box.setChecked(False)

    grade_id = self.grade_selector.currentIndex() + 1
    create_word(word, grade_id, subjects)
    from dialogs.word_update_widget import WordUpdateWidget
    WordUpdateWidget.add_word_to_dictionary(grade_id, word)
    from dialogs.word_family_update_widget import WordFamilyUpdateWidget
    WordFamilyUpdateWidget.update_dictionary_words(word_to_add = word)

  def word_is_invalid(self):
    word = self.word_line_edit.text().strip()
    if len(word) == 0:
      return True, WordAdditionWIdget.WORD_EMPTY_TEXT

    if word_exists(self.grade_selector.currentIndex() + 1, word):
      return True, WordAdditionWIdget.WORD_EXISTS_TEXT

    for character in word:
      if not character in WordAdditionWIdget.GREEK_CHARACTERS:
        return True, WordAdditionWIdget.ONLY_GREEK_CHARACTERS_ALLOWED_TEXT

    for check_box in self.check_boxes:
      if check_box.isChecked():
        return False, ''

    return True, WordAdditionWIdget.NO_SUBJECT_SELECTED_TEXT