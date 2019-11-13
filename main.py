"""
Main script to interact with the data.
"""
import operator

from visualisation import visual
from utils import conversions
from database.db_queries import select_cols
import matplotlib.pyplot as plt
db_path = './database/{0}'
players_db = db_path.format('players.db')


def plot_highest_value_clubs(num_clubs=10):
    """
    Plot the highest value clubs.
    :param num_clubs:
    :return:
    """
    result = select_cols(players_db, select=['Club', 'Value'], _from='players')

    club_value_dict = {}

    for club, value in zip(result['Club'], result['Value']):

        if club not in club_value_dict.keys():
            club_value_dict[club] = 0
        club_value_dict[club] += conversions.convert_money_string(value)
    print(club_value_dict)

    richest_clubs = sorted(club_value_dict.items(), key=operator.itemgetter(1), reverse=True)[:num_clubs]
    labels = [club_name[0] for club_name in richest_clubs]
    values = [value[1] for value in richest_clubs]

    visual.create_bar_chart(values, labels, x_label='Club', y_label='Value(€)',
                            title=f'Top {num_clubs} highest value clubs', horizontal=True)


# Create bar chart of Player wages at Manchester united
result = select_cols(players_db, select=['Name', 'Wage'], _from='players', where='Club="Manchester United"')

convert_wage_str = [conversions.convert_money_string(amount) for amount in result['Wage']]

visual.create_bar_chart(convert_wage_str, result['Name'], x_label='Player', y_label='Wage(€)',
                        title='Manchester United player wages',  horizontal=False)


# Create Scatter plot of Players ages and Overalls
result = select_cols(players_db, ['Age', 'Overall'], _from='players', where='Club="Manchester United"')

visual.create_scatter_plot(result['Age'], result['Overall'], title='Manchester United Age vs Overall',
                           x_label='Age', y_label='Overall', plot_l_r_line=True)


plot_highest_value_clubs(20)


plt.show()
