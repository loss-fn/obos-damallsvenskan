## Predicting OBOS Damallsvenskan 2019 results
## -------------------------------------------

## scrape.py is used to get the match data from OBOS Damallsvenskan
## web site using requests and Beautiful Soup.

import requests
from bs4 import BeautifulSoup

## Data on Damallsvenskan results for 2019 is found on
## https://obosdamallsvenskan.se/spelschema/da_2019_regular, unfortunately
## the data for previous seasons is not available anymore.

def scrape(url = "https://obosdamallsvenskan.se/spelschema/da_2019_regular"):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup

if __name__ == "__main__":
    ## testing it out
    print(scrape())