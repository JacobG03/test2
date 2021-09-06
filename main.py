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

response = requests.get(search_engine_url + target_url, cookies=cookies)
soup = BeautifulSoup(response.text, 'html.parser')

links = soup.find_all("a", {"data-ved": "2ahUKEwjmr5HolujyAhXNzaQKHdXpCpcQFnoECAIQAQ"})

print(soup)