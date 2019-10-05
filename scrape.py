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

def extract(soup):
    result = ["Round,Date,Home,Away,Score", ]

    ## after poking around in the HTML a while it turns out that everything we
    ## need is included inside a number of div elements of class
    ## rmss_c-schedule-game__element.
    games = soup.find_all("div", class_ = "rmss_c-schedule-game__element")
    for game in games:
        round_ = game.find("span", class_ = "rmss_c-schedule-game__info__round-number").text
        date_ = game.find("div", class_ = "rmss_c-schedule-game__extra-button")['data-game-extra'].split('_')[-1]
        home = game.find("div", class_ = "rmss_c-schedule-game__team is-home-team").text.strip().replace('\n', ' ')
        away = game.find("div", class_ = "rmss_c-schedule-game__team is-away-team").text.strip().replace('\n', ' ')
        score = game.find("div", class_ = "rmss_c-schedule-game__result").text.strip().replace('\n', '')

        result.append("%s,%s,%s,%s,%s" % (round_, date_, home, away, score))
    
    return result

def to_csv(result, filename):
    with open(filename, 'w') as f:
        for row in result:
            f.write(row+ '\n')

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description = 'Scrape match data from web site and store in <filename>.')
    parser.add_argument('filename', nargs = 1, help = 'filename of .csv file with extracted match data')
    args = parser.parse_args()

    to_csv(extract(scrape()), args.filename[0])