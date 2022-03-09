from PyQt6.QtGui import QFont

from item.recent_search import RecentSearch

import pickledb

class Settings():
  settings_database_file = 'resources/settings.json'
  font = QFont().family()

  @staticmethod
  def initialize_settings_database(screen_width, screen_height):
    settings_default_values = {
      'maximum_results': 30,
      'last_student_picked': 1,
      'theme': 'light'
    }

    boolean_settings_default_values = {
      'remember_last_student_picked': 0,
      'ask_before_actions': 1,
      'show_edit_dict_words_button': 1,
      'only_show_words_with_family': 0,
      'show_tutorial_on_startup': 1,
      'use_wiktionary': 1
    }

    boolean_settings_about_hiding_messages = [
      'hide_no_internet_message', 'hide_theme_change_effect_message',
      'hide_delete_profile_message', 'hide_delete_student_message',
      'hide_delete_word_message'
    ]

    for key, value in settings_default_values.items():
      if not Settings.get_setting(key):
        Settings.set_setting(key, value)

    for key, value in boolean_settings_default_values.items():
      if isinstance(Settings.get_setting(key), bool):
        Settings.set_setting(key, value)

    for key in boolean_settings_about_hiding_messages:
      Settings.set_setting(key, 0)

    Settings.calculate_size_settings(screen_width, screen_height)

  @staticmethod
  def calculate_size_settings(screen_width, screen_height):
    settings_database = pickledb.load(Settings.settings_database_file, False)
    if not settings_database.get('screen_width') == screen_width:
      settings_database.set('screen_width', screen_width)
      settings_database.set('screen_height', screen_height)

      long_recent_search = RecentSearch('ωωωωωωωωωωωωωωω', True) # 15
      left_widget_width = long_recent_search.sizeHint().width()
      settings_database.set('left_widget_width', left_widget_width)

      right_widget_width = screen_width - left_widget_width - 2
      settings_database.set('right_widget_width', right_widget_width)

      from item.result import Result
      long_result = Result('ωωωωωωωωωωωωωωωωωωωω') # 20
      single_result_width = long_result.sizeHint().width()
      settings_database.set('single_result_width', single_result_width)

      settings_database.dump()

  @staticmethod
  def get_results_widget_columns(widget_width):
    results_widget_columns = (Settings.get_setting('right_widget_width') - 60) // (widget_width + 10)

    return results_widget_columns

  @staticmethod
  def set_boolean_setting(setting_name, setting_value):
    Settings.set_setting(setting_name, 1 if setting_value else 0)

  @staticmethod
  def get_boolean_setting(setting_name):
    return Settings.get_setting(setting_name) == 1

  @staticmethod
  def set_setting(setting_name, setting_value):
    settings_database = pickledb.load(Settings.settings_database_file, False)
    settings_database.set(setting_name, setting_value)
    settings_database.dump()

  @staticmethod
  def get_setting(setting_name):
    settings_database = pickledb.load(Settings.settings_database_file, False)

    return settings_database.get(setting_name)
