"""
Main script to interact with the Fifa 20 dataset.

NOTE: Ensure a GUI backend is installed on your system.
      This is required to use plt.show()
      >> sudo apt-get install python3-tk
"""
import operator
import sys
from collections import OrderedDict

from visualisation import visual, stats
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
                                   title=f'Top {num_clubs} highest value clubs', horizontal=True, save_path='./figures/highest_value_clubs.png')


def plot_highest_value_leagues(player_db, league_db):
    """
    Plot league values.

    :param player_db: Player db
    :type player_db: database.db.DB
    :param league_db: League db
    :type league_db: database.db.DB
    :return: figure and axes for further customization
    :rtype: tuple
    """

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
                                   title=f'League values', horizontal=True, save_path=f'./figures/league_values.png')


def plot_age_pie_chart(player_db):
    """
    Generate a pie chart showing the proportion of players between certain age ranges.

    :param player_db: Player database
    :type player_db: databasae.db.DB
    :return: figure and axes for further customization
    :rtype: tuple
    """

    ages = player_db.select(['Age'])['Age']

    youngest_age = min(ages)
    oldest_age = max(ages)

    print(f'Youngest age: {youngest_age}; Oldest age: {oldest_age}')

    age_brackets = [21, 26, 31, 36, oldest_age]

    age_counts = OrderedDict()
    for i, age_bracket in enumerate(age_brackets):

        if age_bracket == 21:
            # first age bracket, use youngest age
            age_counts[f'{youngest_age}-{age_bracket}'] = len([age for age in ages
                                                               if youngest_age <= age <= age_bracket])
        elif i+1 < len(age_brackets):
            # ensure there is a age bracket left
            age_counts[f'{age_bracket}-{age_brackets[i+1]}'] = len([age for age in ages
                                                                    if age_bracket <= age <= age_brackets[i+1]])

    print(f'Age counts: {age_counts}')

    brackets = age_counts.keys()
    counts = age_counts.values()

    return visual.create_pie_chart(counts, labels=brackets, title='Player age counts',
                                   save_path='./figures/age_brackets.png')


def print_basic_stats_about_team(player_db, team):
    """
    Display some basic stats about the provided team.

    :param player_db: Player DB object
    :type player_db: database.db.DB
    :param team: Name of team
    :type team: str
    :return: tuple -> (average_age, modal_age, average_overall, number_of_players)
    :rtype: tuple
    """

    print(f'Calculating statistics for {team}')

    result = player_db.select(['Age', 'Overall', 'Wage', 'Value'], where=f'Club="{team}"')

    average_age = round(stats.mean(result['Age']), 1)
    modal_age = stats.mode(result['Age'])
    age_deviation = round(stats.standard_deviation(result['Age']), 1)
    print('Team Age:')
    print(f'Mean: {average_age}')
    print(f'Mode: {modal_age}')
    print(f'Deviation: {age_deviation}')

    average_overall = round(stats.mean(result['Overall']), 1)
    modal_overall = stats.mode(result['Overall'])
    overall_deviation = round(stats.standard_deviation(result['Overall']), 1)
    print('Team Overall:')
    print(f'Mean: {average_overall}')
    print(f'Mode: {modal_overall}')
    print(f'Deviation: {overall_deviation}')

    wage_as_num = [conversions.convert_money_string(wage) for wage in result['Wage']]
    average_wage = stats.mean(wage_as_num)
    wage_deviation = stats.standard_deviation(wage_as_num)
    print('Team Wage:')
    print(f'Mean: {average_wage}')
    print(f'Deviation: {wage_deviation}')

    num_players = len(wage_as_num)
    print(f'Number of players: {num_players}')

    return (average_age, modal_age, age_deviation,
            average_overall, modal_overall, overall_deviation,
            average_wage, wage_deviation, num_players)


if __name__ == '__main__':

    ######  Create DB objects ######
    player_db = DB(players_db_path)
    league_db = DB(leagues_db_path)

    ######  Read team name from command line or input ######
    if len(sys.argv) > 1:
        team_name = sys.argv[1]
    else:
        team_name = input('Please enter team name: ')

    ######  Validate the provided team name: Case sensitive ######

    if not player_db.validate_team(team_name):
        raise Exception(f'Invalid team name provided: {team_name}')

    ######  Number of rows in the dataset ######

    entire_dataset = player_db.select(['*'], dict_result=False)
    print(f'\nNumber of rows in the dataset: {len(entire_dataset)}')

    print_basic_stats_about_team(player_db, team_name)

    ###### Generate Plots specific to team ######

    # Create bar chart of Player wages at Manchester united
    result = player_db.select(select=['Name', 'Wage'], where=f'Club="{team_name}"')

    # Wage strings need to be converted to floats for plotting
    convert_wage_str = [conversions.convert_money_string(amount) for amount in result['Wage']]

    visual.create_bar_chart(convert_wage_str, result['Name'], x_label='Player', y_label='Wage(€)',
                            title=f'{team_name} player wages',  horizontal=False, save_path=f'./figures/{team_name}_wages.png')

    # Create Scatter plot of Players ages and Overalls
    result = player_db.select(['Age', 'Overall'], where=f'Club="{team_name}"')
    visual.create_scatter_plot(result['Age'], result['Overall'], title=f'{team_name} Age vs Overall',
                               x_label='Age', y_label='Overall', plot_l_r_line=True, save_path=f'./figures/{team_name}_age_overall.png')

    ###### Generate Plots Generic to dataset ######

    # Plot top 20 highest value clubs
    plot_highest_value_clubs(player_db, 20)

    # Create bar chart of league values
    plot_highest_value_leagues(player_db, league_db)

    # Plot age bracket pie chart
    plot_age_pie_chart(player_db)

    # Show all plots
    plt.show()
