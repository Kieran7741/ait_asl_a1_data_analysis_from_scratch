from urllib import request
from bs4 import BeautifulSoup

import sqlite3


teams_url = 'https://www.skysports.com/football/teams'


def make_the_soup(url):
    """
    Create Beautifulsoup object for the provided url

    :param url: Webpage url
    :type url: str
    :return: BeautifulSoup html parser for provided url
    :rtype: `bs4.BeautifulSoup`
    :raises Exception: if issue downloading webpage
    """

    try:
        html = request.urlopen(url).read()
        return BeautifulSoup(html, 'lxml')
    except Exception as e:
        print(f'Error occurred. Make sure you have an internet connection '
              f'and ensure url[{url}] is valid: {e}')
        raise e


def build_league_map(url):
    """
    Build a league map containing a list of teams in the league

    :param url: Webpage url
    :return: dict of league and teams.
    :rtype: dict
    """

    soup = make_the_soup(url)
    league_map = {}
    league_elements = [el for el in soup.find_all('li', attrs={'class': 'category-list__item accordian__item'})]

    for league in league_elements:
        league_name = league.find('h4', attrs={'class': 'category-list__header'}).text.strip(' \n')
        teams = [team.text.strip() for team in league.find_all('a', attrs={'class': 'category-list__sub-link'})]
        league_map[league_name] = teams

    return league_map


def create_and_populate_clubs_table(url):
    """
    Create the leagues db

    :param url: Webpage to build map db from
    :type url: str
    """

    try:
        league_map = build_league_map(url)
    except Exception as e:
        print(f'Could not generate league map due to {e}')
    else:
        with sqlite3.connect('leagues.db') as connection:
            connection.execute('CREATE TABLE IF NOT EXISTS leagues(league TEXT, team TEXT)')
            for league, teams in league_map.items():
                for team in teams:
                    connection.execute('INSERT INTO leagues VALUES(?,?)', (league, team))


def get_league_for_team(team):
    """
    Get a teams league.
    :param team:
    :return:
    """
    with sqlite3.connect('leagues.db') as connection:
        league = connection.execute('SELECT league FROM leagues WHERE team="{0}"'.format(team))
        return league.fetchall()[0][0]


if __name__ == '__main__':
    print('Running web scrapper.')
    # create_and_populate_clubs_table()

    # print(get_league_for_team('Watford'))
