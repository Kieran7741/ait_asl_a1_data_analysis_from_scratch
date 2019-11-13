"""
Main script to interact with the data.

NOTE: Ensure a GUI backend is installed on your system.
      This is required to use plt.show()
      >> sudo apt-get install python3-tk
"""
import operator

from visualisation import visual
from utils import conversions
from database.db_queries import select_cols
from database.db import DB
import matplotlib.pyplot as plt
db_path = './database/{0}'
players_db_path = db_path.format('players.db')



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
    labels = [club_name[0] for club_name in richest_clubs]
    values = [value[1] for value in richest_clubs]

    return visual.create_bar_chart(values, labels, x_label='Value(€)', y_label='Club',
                                  title=f'Top {num_clubs} highest value clubs', horizontal=True)


if __name__ == '__main__':
    
    # Create DB object
    player_db = DB(players_db_path)

    # Create bar chart of Player wages at Manchester united
    result = player_db.select(select=['Name', 'Wage'], where='Club="Manchester United"')

    # Wage strings need to be converted to floats for plotting
    convert_wage_str = [conversions.convert_money_string(amount) for amount in result['Wage']]

    visual.create_bar_chart(convert_wage_str, result['Name'], x_label='Player', y_label='Wage(€)',
                            title='Manchester United player wages',  horizontal=False)

    # Create Scatter plot of Players ages and Overalls
    result = player_db.select(['Age', 'Overall'], where='Club="Arsenal"')
    visual.create_scatter_plot(result['Age'], result['Overall'], title='Arsenal Age vs Overall',
                            x_label='Age', y_label='Overall', plot_l_r_line=True)

    # Plot top 20 highest value clubs
    plot_highest_value_clubs(player_db, 20)

    # Show all plots
    plt.show()
