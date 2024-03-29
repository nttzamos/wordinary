from bs4 import BeautifulSoup

import requests

def fetch_online_results(word):
  if not active_internet_connection_exists(): raise RuntimeError

  url = 'https://el.wiktionary.org/wiki/{}'
  session = requests.Session()

  try:
    session.mount('https://', requests.adapters.HTTPAdapter(max_retries = 2))
  except Exception as e:
    print('Retries did not work.')

  response = session.get(url.format(word))
  if response.status_code != 200:
    if response.status_code != 404:
      print('Wrong Status')
    return []

  soup = BeautifulSoup(response.text.replace('>\n<', '><'), 'html.parser')

  online_results = set()

  compound_words_header = soup.find(id='Σύνθετα')
  if compound_words_header != None:
    compound_words_list = compound_words_header.find_next('ul')
    for item in compound_words_list.find_all():
      if item_is_valid(item):
        word_to_be_added = clean_word(item.text.lower())
        if len(word_to_be_added) > 0:
          online_results.add(word_to_be_added)

  related_words_header = soup.find(id='Συγγενικές_λέξεις')
  if related_words_header != None:
    related_words_list = related_words_header.find_next('ul')
    for item in related_words_list.find_all():
      if item_is_valid(item):
        word_to_be_added = clean_word(item.text.lower())
        if len(word_to_be_added) > 0:
          online_results.add(word_to_be_added)

  return list(online_results)

def active_internet_connection_exists():
  try:
    requests.get(url = 'https://www.google.com', timeout = 1)
  except (requests.ConnectionError, requests.Timeout) as exception:
    return False

  return True

def item_is_valid(item):
  if item.name != 'li':
    return False

  forbidden_substrings = ['δείτε', '-']
  for substring in forbidden_substrings:
    if substring in item.text:
      return False

  return True

def clean_word(word):
  forbidden_characters = [',', '(', ' και', '/', '&']
  for character in forbidden_characters:
    new_word = word.split(character)[0]
    if character == '(' and not new_word:
      try:
        new_word = word.split(')')[1]
      except Exception as e:
        print(word)

    word = new_word

  # If after all of the processing the string still consists of multiple words
  # then we return an empty string so that the word is not added to the results.
  if len(word.split()) > 1: return ''

  return word.strip()
