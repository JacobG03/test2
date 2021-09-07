import requests
from bs4 import BeautifulSoup
from os.path import join, dirname
from os import environ
from dotenv import load_dotenv
import time


# Loads .env variables
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Needed in order to avoid google cookie verification
# SID cookie value
sid = environ.get('SID')

search_engine_url = 'https://www.google.com/search?q='
target_url = 'site:https://www.searchenginejournal.com/'
pagination = '&start='

cookies = {
  'SID': sid,
}

headers = {'User-agent': 'agent 0.1'}


# Read's and returns a list of keywords
def getKeywords():
  with open('keywords.txt', 'r') as file:
    data = file.read().replace('\n', '')  
  return data.split(',')


# keywords = [], pages = int
def getLinks(keywords, pages):
  results = []
  for count, word in enumerate(keywords):
    links = []
    total_results = None

    query = f'{search_engine_url}{target_url}%20{word}'

    for i in range(pages):
      paginated_query = f'{query}{pagination}{i * 10}'

      response = requests.get(paginated_query, headers=headers, cookies=cookies)
      soup = BeautifulSoup(response.text, 'html.parser')

      if total_results == None:
        total_results = getTotalResults(soup)

      parent_divs = soup.find_all("div", {"class": "kCrYT"})

      for element in parent_divs:
        a = element.find('a', href=True)
        if a:
          valid = validateHref(a['href'])
          if valid['valid']:
            links.append(valid['href'])
      
      print(f'Page {i + 1}/{pages}')
      # Pause to avoid getting blocked
      time.sleep(10)
      
      # also find max results here and append with links
    results.append({
      word: {
        'links': links,
        'results': total_results
        }
      })
    print(f'{count + 1}/{len(keywords)}')

  return results


def getTotalResults(soup):
  # Get the total result data using selenium
  return 'Unknown'

# Returns a valid link
def validateHref(href):
  href = href.split('/')
  if '&' in href[4] or '&' in href[5]:
    return {'valid': False}
  try:
    link = f'https://{href[3]}/{href[4]}/{href[5]}'
  except:
    link = f'https://{href[3]}/{href[4]}'

  return {'valid': True, 'href': link}


keywords = getKeywords()
results = getLinks(keywords, 3)
print(results)