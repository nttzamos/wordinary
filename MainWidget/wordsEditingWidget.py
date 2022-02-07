from PyQt6.QtWidgets import QVBoxLayout, QLineEdit, QComboBox, QDialog, QLabel, QCompleter, QCheckBox, QRadioButton, QWidget, QHBoxLayout, QMessageBox, QGroupBox
from PyQt6.QtCore import QStringListModel, QTimer, Qt
from PyQt6.QtGui import QFont, QIcon

from MenuBar.settings import Settings
from Common.databaseHandler import DBHandler

class WordsEditingWidget(QDialog):
  def __init__(self):
    super().__init__()
    self.setWindowTitle('Edit Dictionary Words')
    self.setWindowIcon(QIcon("Resources/windowIcon.svg"))

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(20, 0, 20, 15)
    self.layout.setSpacing(0)

    labelFont = QFont(Settings.font, 12)
    comboBoxFont = QFont(Settings.font, 14)
    radioButtonFont = QFont(Settings.font, 14)
    checkBoxFont = QFont(Settings.font, 14)
    lineEditFont = QFont(Settings.font, 14)
    completerFont = QFont(Settings.font, 12)
    sectionLabelFont = QFont(Settings.font, 16)
    errorMessageFont = QFont(Settings.font, 10)

    self.gradeSelector = QComboBox()
    self.gradeSelector.activated.connect(self.updateWordsList)
    self.gradeSelector.setFont(comboBoxFont)
    self.gradeSelector.addItems(DBHandler.getGrades())

    gradeSelectionWidget = QGroupBox('Grade Selection')
    gradeSelectionWidget.setFont(sectionLabelFont)
    gradeSelectionWidget.layout = QVBoxLayout(gradeSelectionWidget)
    gradeSelectionWidget.layout.setContentsMargins(10, 10, 10, 10)
    gradeSelectionWidget.layout.addWidget(self.gradeSelector)

    self.updateSelectionButton = QRadioButton('Update Word')
    self.updateSelectionButton.setFont(radioButtonFont)
    self.deletionSelectionButton = QRadioButton('Delete Word')
    self.deletionSelectionButton.setFont(radioButtonFont)
    if Settings.getDefaultEditingAction() == 'update':
      self.updateSelectionButton.setChecked(True)
    else:
      self.deletionSelectionButton.setChecked(True)

    self.updateSelectionButton.toggled.connect(self.updateButtonToggled)
    self.deletionSelectionButton.toggled.connect(self.deleteButtonToggled)

    actionSelectionButtons = QWidget()
    actionSelectionButtons.layout = QHBoxLayout(actionSelectionButtons)
    actionSelectionButtons.layout.setContentsMargins(0, 0, 0, 0)
    actionSelectionButtons.layout.addWidget(self.updateSelectionButton)
    actionSelectionButtons.layout.addWidget(self.deletionSelectionButton)

    actionSelectionWidget = QGroupBox('Action Selection')
    actionSelectionWidget.setFont(sectionLabelFont)
    actionSelectionWidget.layout = QVBoxLayout(actionSelectionWidget)
    actionSelectionWidget.layout.setContentsMargins(10, 10, 10, 10)
    actionSelectionWidget.layout.addWidget(actionSelectionButtons)

    self.updateAllGrades = QCheckBox('Update/Delete word for all grades?')
    self.updateAllGrades.setFont(checkBoxFont)

    self.showCandidates = QCheckBox('Show only candidate words for update/deletion?')
    self.showCandidates.setFont(checkBoxFont)
    self.showCandidates.toggled.connect(self.updateWordsList)

    parametersConfigurationWidget = QGroupBox('Parameter Configuration')
    parametersConfigurationWidget.setFont(sectionLabelFont)
    parametersConfigurationWidget.layout = QVBoxLayout(parametersConfigurationWidget)
    parametersConfigurationWidget.layout.setContentsMargins(10, 10, 10, 10)
    parametersConfigurationWidget.layout.addWidget(self.updateAllGrades)
    parametersConfigurationWidget.layout.addWidget(self.showCandidates)

    wordSelectionLabel = QLabel('Word Selection')
    wordSelectionLabel.setFont(labelFont)
    self.wordSelectionLineEdit = QLineEdit()
    self.wordSelectionLineEdit.setFont(lineEditFont)
    self.wordSelectionLineEdit.returnPressed.connect(self.wordSelected)
    self.dictionaryWords = DBHandler.getGradeWords(1)
    self.completer = QCompleter(self.dictionaryWords)
    self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    self.completer.popup().setFont(completerFont)
    self.wordSelectionLineEdit.setCompleter(self.completer)
    self.wordSelectionLineEdit.setPlaceholderText('Please enter a word.')
    self.wordSelectionLineEdit.textChanged.connect(self.searchTextChanged)
    self.errorMessageLabel = QLabel("Please search for another word", self)
    self.errorMessageLabel.setFont(errorMessageFont)
    sizePolicy = self.errorMessageLabel.sizePolicy()
    sizePolicy.setRetainSizeWhenHidden(True)
    self.errorMessageLabel.setSizePolicy(sizePolicy)
    self.showErrorMessage = False

    self.updateWordWidget = QWidget()
    self.updateWordWidget.layout = QVBoxLayout(self.updateWordWidget)
    self.updateWordWidget.layout.setContentsMargins(0, 0, 0, 0)
    updateFormLabel = QLabel('Editing Form')
    updateFormLabel.setFont(labelFont)
    self.wordEditingLineEdit = QLineEdit()
    self.wordEditingLineEdit.setFont(lineEditFont)
    self.wordEditingLineEdit.returnPressed.connect(self.updateWordConfirmation)
    self.wordEditingLineEdit.setPlaceholderText('You have to select a word first.')
    self.wordEditingLineEdit.setDisabled(True)
    self.updateWordWidget.layout.setSpacing(5)
    self.updateWordWidget.layout.addWidget(updateFormLabel)
    self.updateWordWidget.layout.addWidget(self.wordEditingLineEdit)

    wordEditingWidget = QGroupBox('Word Editing')
    wordEditingWidget.setFont(sectionLabelFont)
    wordEditingWidget.layout = QVBoxLayout(wordEditingWidget)
    wordEditingWidget.layout.setContentsMargins(10, 10, 10, 10)
    wordEditingWidget.layout.setSpacing(0)
    wordEditingWidget.layout.addWidget(wordSelectionLabel)
    wordEditingWidget.layout.addSpacing(5)
    wordEditingWidget.layout.addWidget(self.wordSelectionLineEdit)
    wordEditingWidget.layout.addWidget(self.errorMessageLabel, alignment=Qt.AlignmentFlag.AlignRight)
    self.errorMessageLabel.hide()
    wordEditingWidget.layout.addWidget(self.updateWordWidget)
    if self.deletionSelectionButton.isChecked():
      self.updateWordWidget.hide()

    self.layout.addWidget(gradeSelectionWidget)
    self.layout.addSpacing(15)

    self.layout.addWidget(actionSelectionWidget)
    self.layout.addSpacing(15)

    self.layout.addWidget(parametersConfigurationWidget)
    self.layout.addSpacing(15)

    self.layout.addWidget(wordEditingWidget)

    self.wordSelectionLineEdit.setFocus()

    self.style()

  def style(self):
    from Common.styles import Styles
    self.setStyleSheet(Styles.wordsEditingWidgetStyle)
    self.errorMessageLabel.setStyleSheet(Styles.errorMessageLabelStyle)

  def wordSelected(self):
    self.searchedWord = self.wordSelectionLineEdit.text()
    if self.searchedWord in self.dictionaryWords:
      if self.updateSelectionButton.isChecked():
        self.wordEditingLineEdit.setText(self.searchedWord)
        self.wordEditingLineEdit.setEnabled(True)
        self.wordEditingLineEdit.setFocus()
      elif self.deletionSelectionButton.isChecked():
        self.deleteWordConfirmation()
    else:
      self.showErrorMessage = True
      self.errorMessageLabel.show()

  def searchTextChanged(self):
    if self.showErrorMessage:
      self.showErrorMessage = False
      self.errorMessageLabel.hide()

  def updateWordConfirmation(self):
    if Settings.getBooleanSetting('askBeforeActions'):
      newWord = self.wordEditingLineEdit.text()
      title = 'Update Word'
      question = "Are you sure you want to update '" + self.searchedWord + "' to '" + newWord + "'?"
      answer = QMessageBox.question(self, title, question, QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Yes)
      if answer == QMessageBox.StandardButton.Yes:
        self.updateWord()
    else:
      self.updateWord()

  def updateWordsList(self, unusedVariable):
    if self.showCandidates.isChecked():
      self.dictionaryWords = DBHandler.getCandidateWords(self.gradeSelector.currentIndex() + 1)
    else:
      self.dictionaryWords = DBHandler.getGradeWords(self.gradeSelector.currentIndex() + 1)

    model = QStringListModel(self.dictionaryWords, self.completer)
    self.completer.setModel(model)

  def updateWord(self):
    newWord = self.wordEditingLineEdit.text()
    DBHandler.updateWord(self.searchedWord, newWord, self.getGrades())
    self.updateDictionaryWords(self.searchedWord, newWord)
    QTimer.singleShot(0, self.wordSelectionLineEdit.clear)
    QTimer.singleShot(0, self.wordEditingLineEdit.clear)
    self.wordEditingLineEdit.setDisabled(True)
    self.wordSelectionLineEdit.setFocus()

  def deleteWordConfirmation(self):
    if Settings.getBooleanSetting('askBeforeActions'):
      title = 'Delete Word'
      question = "Are you sure you want to delete '" + self.searchedWord + "'?"
      answer = QMessageBox.question(self, title, question, QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Yes)
      if answer == QMessageBox.StandardButton.Yes:
        self.deleteWord()
    else:
      self.deleteWord()

  def deleteWord(self):
    DBHandler.deleteWord(self.searchedWord, self.getGrades())
    self.updateDictionaryWords(self.searchedWord)
    QTimer.singleShot(0, self.wordSelectionLineEdit.clear)

  def deleteButtonToggled(self):
    if self.deletionSelectionButton.isChecked():
      QTimer.singleShot(0, self.wordEditingLineEdit.clear)
      self.wordEditingLineEdit.setDisabled(True)
      self.updateWordWidget.hide()

  def updateButtonToggled(self):
    if self.updateSelectionButton.isChecked():
      self.updateWordWidget.show()

  def getGrades(self):
    grades = []
    if self.updateAllGrades.isChecked():
      grades = list(range(1, 7))
    else:
      grades.append(self.gradeSelector.currentIndex() + 1)

    return grades

  def updateDictionaryWords(self, oldWord, newWord=None):
    if not (newWord == None or newWord in self.dictionaryWords):
      self.dictionaryWords.append(newWord)

    self.dictionaryWords.remove(oldWord)
    model = QStringListModel(self.dictionaryWords, self.completer)
    self.completer.setModel(model)
