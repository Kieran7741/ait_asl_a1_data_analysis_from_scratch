"""
Main script to interact with the data.
"""

from visualisation import visual, stats
from database.db_queries import select_cols
import matplotlib.pyplot as plt
db_path = './database/{0}'
players_db = db_path.format('players.db')


def convert_money_string(money_str):
    """
    Convert a wage of the form $200k to 200000
    :param money_str:
    :return: Amount as float
    """

    multiplier = 1000 if money_str[-1].lower() == 'k' else 10000000

    return float(money_str[1:-1]) * multiplier


# Create bar chart of Player wages at Manchester united
result = select_cols(players_db, select=['Name', 'Wage'], _from='players', where='Club="Manchester United"')
convert_wage_str = [convert_money_string(amount) for amount in result['Wage']]
visual.create_bar_chart(result['Name'], convert_wage_str, x_label='Player', y_label='Wage(€)', horizontal=False)

# Create Scatter plot of Players ages and Overalls

result = select_cols(players_db, ['Age', 'Overall'], _from='players', where='Club="Manchester United"')
visual.create_scatter_plot(result['Age'], result['Overall'], title='Manchester United Age vs Overall',
                           x_label='Age', y_label='Overall', plot_l_r_line=True)


plt.show()
