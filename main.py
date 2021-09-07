from typing import Counter
import requests
from bs4 import BeautifulSoup
from os.path import join, dirname
from os import environ
from dotenv import load_dotenv


# Loads .env variables
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Needed in order to avoid google cookie verification
# SID cookie value
sid = environ.get('SID')

search_engine_url = 'https://www.google.com/search?q='
target_url = 'site:https://www.searchenginejournal.com/'

cookies = {
  'SID': sid,
}


# Read's and returns a list of keywords
def getKeywords():
  with open('keywords.txt', 'r') as file:
    data = file.read().replace('\n', '')  
  return data.split(',')


# keywords = [], pages = int
def getLinks(keywords, pages):
  results = []
  for count, word in enumerate(keywords):
    query = f'{search_engine_url}{target_url} {word}'

    response = requests.get(query, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')

    parent_divs = soup.find_all("div", {"class": "kCrYT"})

    links = []
    for element in parent_divs:
      a = element.find('a', href=True)
      if a:
        valid = validateHref(a['href'])
        if valid['valid']:
          print(valid['href'])
          links.append(valid['href'])
    
    # also find max results here and append with links
    results.append({word: links})
    print(f'{count + 1}/{len(keywords)}')

  return results


def validateHref(href):
  href = href.split('/')

  for i in href:
    try:
      i = int(i)

      index = href.index(str(i))
      href = f'https://{href[index - 2]}/{href[index - 1]}/{str(i)}'

      return {'valid': True, 'href': href}
    except:
      pass
  return {'valid': False, 'href': href}


results = getLinks(getKeywords(), 5)
print(results)