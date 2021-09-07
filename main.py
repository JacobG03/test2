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



response = requests.get(search_engine_url + target_url + ' tutorial', cookies=cookies)
soup = BeautifulSoup(response.text, 'html.parser')


# Make it so that class is a variable working on every pc
parent_divs = soup.find_all("div", {"class": "kCrYT"})

links = []

for element in parent_divs:
  a = element.find('a', href=True)
  if a:
    #! Format link
    #* Remove string after /6 ditit number/ remove
    links.append(a['href'])

print(links)