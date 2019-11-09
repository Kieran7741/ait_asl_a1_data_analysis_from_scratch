from urllib import request
from bs4 import BeautifulSoup

import sqlite3


teams_url = 'https://www.skysports.com/football/teams'


def make_the_soup(url):
    html = request.urlopen(url).read()
    return BeautifulSoup(html, 'lxml')


def build_league_map(url):
    soup = make_the_soup(url)
    league_map = {}
    league_elements = [el for el in soup.find_all('li', attrs={'class': 'category-list__item accordian__item'})]

    for league in league_elements:
        league_name = league.find('h4', attrs={'class': 'category-list__header'}).text.strip(' \n')
        teams = [team.text.strip() for team in league.find_all('a', attrs={'class': 'category-list__sub-link'})]
        league_map[league_name] = teams

    return league_map


def create_and_populate_clubs_table():

    league_map = build_league_map(teams_url)
    connection = sqlite3.connect('leagues.db')
    connection.execute('CREATE TABLE IF NOT EXISTS leagues(league TEXT, team TEXT)')
    for league, teams in league_map.items():
        for team in teams:
            connection.execute('INSERT INTO leagues VALUES(?,?)', (league, team))

    connection.commit()
    connection.close()


def get_league_for_team(team):

    connection = sqlite3.connect('leagues.db')
    league = connection.execute('SELECT league FROM leagues WHERE team="{0}"'.format(team))
    return league.fetchall()[0][0]

# create_and_populate_clubs_table()

print(get_league_for_team('Watford'))
