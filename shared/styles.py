class Styles():
  from menu.settings import Settings
  theme = Settings.get_setting('theme')

  if theme == 'light':
    menu_bar_style = """
      QPushButton:hover { background-color: grey }
      QPushButton { border: none }
      QPushButton { padding-bottom: 5px }
      QPushButton { padding-top: 5px }
      QLabel { color: black }"""
  else:
    menu_bar_style = """
      QPushButton:hover { background-color: grey }
      QPushButton { border: none }
      QPushButton { padding-bottom: 5px }
      QPushButton { padding-top: 5px }
      QLabel { color: white }"""

  application_icon_style = """QPushButton:hover { background-color: none }"""

  if theme == 'light':
    settings_widget_style = """
      QCheckBox { color: black }
      QRadioButton { color: black }"""
  else:
    settings_widget_style = """
      QWidget { background-color: #171010 }
      QCheckBox { color: white }
      QRadioButton { color: white }"""

  if theme == 'light':
    close_window_button_style = """
      QPushButton:hover { background-color: #D11A2A }"""
  else:
    close_window_button_style = """
      QPushButton:hover { background-color: #D11A2A }"""

  if theme == 'light':
    main_window_style = """
      QWidget { background-color: #FFFAFA }
      QPushButton { background-color: none }"""
  else:
    main_window_style = """
      QWidget { background-color: #2B2B2B }
      QPushButton { background-color: none }"""

  if theme == 'light':
    main_window_background_style = """
      QWidget { background-color: #FFFAFA }\n
      QPushButton { background-color: none }"""
  else:
    main_window_background_style = """
      QWidget { background-color: #171010 }\n
      QPushButton { background-color: none }"""

  if theme == 'light':
    side_widgets_style = """
      QWidget { background-color: #DEDEDE }
      QLabel { color: black; padding: 0px 10px }
      QScrollBar { background-color: none }"""
  else:
    side_widgets_style = """
      QWidget { background-color: #362222 }
      QLabel { color: white; padding: 0px 10px }
      QScrollBar { background-color: none }"""

  if theme == 'light':
    side_widgets_title_label_style = """
      QLabel { border: 1px solid black; border-bottom: 0px; padding: 10px 0px; background-color: #F9E4C8; color: #1C1C1C }"""
  else:
    side_widgets_title_label_style = """
      QLabel { border: 1px solid white; border-bottom: 0px; padding: 10px 0px; background-color: #423F3E; color: white }"""

  if theme == 'light':
    item_widgets_style = """
      QWidget { background-color: #FBF7F0 }
      QLabel { color: black }
      QPushButton:hover { background-color: grey }
      QPushButton { border: 1px solid black }
      QPushButton { padding-bottom: 5px }
      QPushButton { padding-top: 5px }
      QPushButton { background-color: none }"""
  else:
    item_widgets_style = """
      QWidget { background-color: #171010 }
      QLabel { color: white }
      QPushButton:hover { background-color: grey }
      QPushButton { border: 1px solid white }
      QPushButton { padding-bottom: 5px }
      QPushButton { padding-top: 5px }
      QPushButton { background-color: white }"""

  if theme == 'light':
    searching_widget_focused_style = """
      QWidget { background-color: white; border-radius: 10px; border: 1px solid blue }
      QLineEdit { border: none }
      QPushButton { background-color: none }
      QPushButton { border: none }
      QPushButton { padding-bottom: 8px }
      QPushButton { padding-top: 8px }"""
  else:
    searching_widget_focused_style = """
      QWidget { background-color: white; border-radius: 10px; border: 1px solid blue }
      QLineEdit { border: none }
      QPushButton { background-color: none }
      QPushButton { border: none }
      QPushButton { padding-bottom: 8px }
      QPushButton { padding-top: 8px }"""

  if theme == 'light':
    searching_widget_error_style = """
      QWidget { background-color: white; border-radius: 10px; border: 1px solid red }
      QLineEdit { border: none }
      QPushButton { background-color: none }
      QPushButton { border: none }
      QPushButton { padding-bottom: 8px }
      QPushButton { padding-top: 8px }"""
  else:
    searching_widget_error_style = """
      QWidget { background-color: white; border-radius: 10px; border: 1px solid red }
      QLineEdit { border: none }
      QPushButton { background-color: none }
      QPushButton { border: none }
      QPushButton { padding-bottom: 8px }
      QPushButton { padding-top: 8px }"""

  if theme == 'light':
    subwidget_style = """
      QPushButton { border: 1px solid black; border-radius: 10px; padding: 5px 50px }
      QPushButton { color: black; border-bottom: 3px solid black; border-right: 3px solid black }
      QPushButton:hover { background-color: grey }"""
  else:
    subwidget_style = """
      QPushButton { border: 1px solid white; border-radius: 10px; padding: 5px 50px }
      QPushButton { color: white }
      QPushButton:hover { background-color: grey }"""

  if theme == 'light':
    error_message_style = """
      QLabel { color: red }
      QLabel { background-color: none }
      QLabel { border: none }"""
  else:
    error_message_style = """
      QLabel { color: red }
      QLabel { background-color: none }
      QLabel { border: none }"""

  if theme == 'light':
    words_editing_widget_style = """
      QWidget { background-color: none }
      QDialog { background-color: #FFFAFA }
      QComboBox { color: black }
      QCheckBox { color: black }
      QRadioButton { color: black }
      QLabel { color: black }"""
  else:
    words_editing_widget_style = """
      QWidget { background-color: none }
      QDialog { background-color: #171010 }
      QComboBox { color: black }
      QCheckBox { color: white }
      QRadioButton { color: white }
      QLabel { color: white }"""

  if theme == 'light':
    error_message_label_style = """QLabel { color: red }"""
  else:
    error_message_label_style = """QLabel { color: red }"""

  if theme == 'light':
    current_search_style = """
      QWidget { background-color: none }
      QPushButton { border: 1px solid black; border-radius: 10px; padding: 5px 30px }
      QPushButton { color: black; border-bottom: 3px solid black; border-right: 3px solid black }
      QPushButton:hover { background-color: grey }
      QComboBox { color: black }"""
  else:
    current_search_style = """
      QWidget { background-color: none }
      QPushButton { border: 1px solid black; border-radius: 10px; padding: 5px 30px }
      QPushButton { color: black }
      QPushButton:hover { background-color: grey }
      QComboBox { color: black }"""

  if theme == 'light':
    searched_word_style = """
      QLabel { border: 1px solid black; padding: 10px 30px; background-color: #F9E4C8; color: black }"""
  else:
    searched_word_style = """
      QLabel { border: 1px solid white; padding: 0px 30px; background-color: #423F3E; color: white }"""

  if theme == 'light':
    results_widget_style = """
      QWidget { background-color: #DEDEDE }
      QLabel { color: black }
      QScrollBar { background-color: none }"""
  else:
    results_widget_style = """
      QWidget { background-color: #362222 }
      QLabel { color: white }
      QScrollBar { background-color: none }"""

  if theme == 'light':
    offline_result_style = """
      QWidget { background-color: white; border-radius: 10px; border: 2px solid black }
      QPushButton { background-color: white }
      QPushButton:hover { background-color: grey }
      QPushButton { border-radius: 12px }
      QPushButton { border: 1px solid black }
      QPushButton { padding-bottom: 5px }
      QPushButton { padding-top: 5px }
      QLabel { color: black; border-radius: none; border: none; background-color: none; padding: 0px 20px }"""
  else:
    offline_result_style = """
      QWidget { background-color: black; border-radius: 10px}
      QPushButton { background-color: white }
      QPushButton:hover { background-color: grey }
      QPushButton { border-radius: 12px }
      QPushButton { border: 1px solid black }
      QPushButton { padding-bottom: 5px }
      QPushButton { padding-top: 5px }
      QLabel { color: white }"""

  if theme == 'light':
    online_result_style = """
      QWidget { background-color: white; border-radius: 10px; border: 2px solid blue }
      QPushButton { background-color: white }
      QPushButton:hover { background-color: grey }
      QPushButton { border-radius: 12px }
      QPushButton { border: 1px solid black }
      QPushButton { padding-bottom: 5px }
      QPushButton { padding-top: 5px }
      QLabel { color: black; border-radius: none; border: none; background-color: none; padding: 0px 20px }"""
  else:
    online_result_style = """
      QWidget { background-color: white; border-radius: 10px; border: 2px solid blue }
      QPushButton { background-color: white }
      QPushButton:hover { background-color: grey }
      QPushButton { border-radius: 12px }
      QPushButton { border: 1px solid black }
      QPushButton { padding-bottom: 5px }
      QPushButton { padding-top: 5px }
      QLabel { color: black; border-radius: none; border: none; background-color: none }"""

  if theme == 'light':
    result_buttons_style = """
      QWidget { background-color: none; border-radius: none; border: none }
      QPushButton { background-color: white }
      QPushButton:hover { background-color: grey }
      QPushButton { border-radius: 12px }
      QPushButton { border: 1px solid black }
      QPushButton { padding-bottom: 5px }
      QPushButton { padding-top: 5px }"""
  else:
    result_buttons_style = """
      QWidget { background-color: none; border-radius: none; border: none }
      QPushButton { background-color: white }
      QPushButton:hover { background-color: grey }
      QPushButton { border-radius: 12px }
      QPushButton { border: 1px solid black }
      QPushButton { padding-bottom: 5px }
      QPushButton { padding-top: 5px }"""

  if theme == 'light':
    legend_button_style = """
      QPushButton { border: 1px solid black; border-radius: 10px; padding: 5px 5px }
      QPushButton:hover { background-color: grey }"""
  else:
    legend_button_style = """
      QPushButton { border: 1px solid black; border-radius: 10px; padding: 5px 5px }
      QPushButton:hover { background-color: grey }"""

  if theme == 'light':
    tutorial_widget_style = """
      QLabel { padding-bottom: 5px }
      QLabel { padding-top: 5px }"""
  else:
    tutorial_widget_style = """
      QLabel { padding-bottom: 5px }
      QLabel { padding-top: 5px }"""

  if theme == 'light':
    dialog_button_style = """
      QWidget { border: none; background-color: none; border-radius: 10px }
      QPushButton { padding: 3px 5px; background-color: white }
      QPushButton:hover { background-color: white }"""
  else:
    dialog_button_style = """
      QWidget { border: none; background-color: none; border-radius: 10px }
      QPushButton { padding: 3px 5px; background-color: white }
      QPushButton:hover { background-color: white }"""

  if theme == 'light':
    dialog_default_button_style = """
      QWidget { border: none; background-color: none; border-radius: 10px }
      QPushButton { padding: 3px 5px; background-color: #007AFF; color: white }
      QPushButton:hover { background-color: #007AFF }"""
  else:
    dialog_default_button_style = """
      QWidget { border: none; background-color: none; border-radius: 10px }
      QPushButton { padding: 3px 5px; background-color: #007AFF; color: white }
      QPushButton:hover { background-color: #007AFF }"""
