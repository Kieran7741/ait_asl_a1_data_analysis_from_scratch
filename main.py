"""
Main script to interact with the Fifa 20 dataset.

NOTE: Ensure a GUI backend is installed on your system.
      This is required to use plt.show()
      >> sudo apt-get install python3-tk
"""
import operator
import sys

from visualisation import visual
from utils import conversions
from database.db import DB
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('TkAgg')


db_path = './database/{0}'
players_db_path = db_path.format('players.db')
leagues_db_path = db_path.format('leagues.db')


def get_cost_of_team(db, team):
    """
    Calculates the cost of a team based on player values.
    :param db: player.db instance
    :type db: database.db.DB
    :param team: Team name
    :type team: str
    :return: total cost of team
    """
    result = db.select(['Value'], where=f'Club="{team}"')['Value']
    return sum([conversions.convert_money_string(value) for value in result])


def plot_highest_value_clubs(db, num_clubs=10):
    """
    Plot the highest value clubs.
    :param db: DB object
    :type db: `database.DB`
    :param num_clubs: Number of clubs to display
    :type num_clubs: int
    :return: figure and axes for further customization
    :rtype: tuple
    """

    result = db.select(select=['Club', 'Value'])

    club_value_dict = {}

    for club, value in zip(result['Club'], result['Value']):

        if club not in club_value_dict.keys():
            club_value_dict[club] = 0
        club_value_dict[club] += conversions.convert_money_string(value)

    richest_clubs = sorted(club_value_dict.items(), key=operator.itemgetter(1), reverse=True)[:num_clubs]
    print(f'\nHighest value clubs: {richest_clubs}')

    # prepare chart
    labels = [club_name[0] for club_name in richest_clubs]
    values = [value[1] for value in richest_clubs]

    return visual.create_bar_chart(values, labels, x_label='Value(€)', y_label='Club',
                                   title=f'Top {num_clubs} highest value clubs', horizontal=True)


def plot_highest_value_leagues(player_db, league_db):

    all_team_leagues = league_db.select(['League', 'Team'], dict_result=False)

    league_map = {}
    for league, team in all_team_leagues:
        if league not in league_map.keys():
            league_map[league] = 0
        league_map[league] += get_cost_of_team(player_db, team)

    richest_leagues = sorted(league_map.items(), key=operator.itemgetter(1), reverse=True)
    print(f'\nLeague values: {richest_leagues}')

    # Prepare Chart
    labels = [league_name[0] for league_name in richest_leagues]
    values = [value[1] for value in richest_leagues]
    return visual.create_bar_chart(values, labels, x_label='Value(€ Billion)', y_label='League',
                                   title=f'League values', horizontal=True)


if __name__ == '__main__':

    # Create DB objects
    player_db = DB(players_db_path)
    league_db = DB(leagues_db_path)

    # Read team name from command line or input
    if len(sys.argv) > 1:
        team_name = sys.argv[1]
    else:
        team_name = input('Please enter team name: ')

    # Validate the provided team name: Case sensitive
    if not player_db.validate_team(team_name):
        raise Exception(f'Invalid team name provided: {team_name}')

    # Some number associated with the dataset
    entire_dataset = player_db.select(['*'], dict_result=False)
    print(f'\nNumber of rows in the dataset: {len(entire_dataset)}')
    # Generate Plots

    # Create bar chart of Player wages at Manchester united
    result = player_db.select(select=['Name', 'Wage'], where=f'Club="{team_name}"')

    # Wage strings need to be converted to floats for plotting
    convert_wage_str = [conversions.convert_money_string(amount) for amount in result['Wage']]

    visual.create_bar_chart(convert_wage_str, result['Name'], x_label='Player', y_label='Wage(€)',
                            title=f'{team_name} player wages',  horizontal=False)

    # Create Scatter plot of Players ages and Overalls
    result = player_db.select(['Age', 'Overall'], where=f'Club="{team_name}"')
    visual.create_scatter_plot(result['Age'], result['Overall'], title=f'{team_name} Age vs Overall',
                               x_label='Age', y_label='Overall', plot_l_r_line=True)

    # Plot top 20 highest value clubs
    plot_highest_value_clubs(player_db, 20)

    # Create bar chart or league values
    plot_highest_value_leagues(player_db, league_db)

    # Show all plots
    plt.show()
