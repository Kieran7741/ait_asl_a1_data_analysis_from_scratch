
import matplotlib.pyplot as plt
from matplotlib import style
from sqlite3 import connect
from visualisation.stats import get_cords_for_best_fit_line

style.use('ggplot')


def get_team_age_overall(team_name):
    """
    Get each players age and overall for the given team name.
    :param team_name: Target team
    :type team_name: str
    :return:
    """
    with connect('players.db') as conn:
        result = conn.execute(f'SELECT Age, Overall FROM players WHERE Club="{team_name}"')

    players = result.fetchall()

    ages = [player[0] for player in players]
    overalls = [player[1] for player in players]
    return ages, overalls


def create_scatter_plot(x_values, y_values, x_label='', y_label='', title='', plot_l_r_line=False, save_path=None):
    """
    Create a scatter plot.
    :param x_values: x axis values
    :type x_values: list
    :param y_values: y axis values
    :type y_values: list
    :param x_label: x axis label
    :type x_label: str
    :param y_label: y axis label
    :type y_label: str
    :param title: Plot title
    :type title: str
    :param plot_l_r_line: Plot the linear regression line.
    :type plot_l_r_line: bool
    :param save_path: Path to save figure to.
    :type save_path: str
    :return: figure and axes for further customization
    :rtype: tuple
    """

    fig, ax = plt.subplots()

    ax.scatter(x_values, y_values)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    if title:
        fig.canvas.set_window_title(title)
        ax.set_title(title)

    if plot_l_r_line:
        c1 , c2 = get_cords_for_best_fit_line(x_values, y_values)
        ax.plot([c1[0], c2[0]], [c1[1], c2[1]], label='Line of best fit', color='black')
        plt.legend()

    if save_path:
        fig.savefig(save_path, bbox_inches='tight')


def create_pie_chart(values, labels, x_label='', y_label='', title='', save_path=None):
    """
    Create a pie chart.
    :param values: Segment totals.
    :type: list or tuple
    :param labels: Segment labels
    :type: list or tuple
    :param x_label: x axis label
    :type x_label: str
    :param y_label: y axis label
    :type y_label: str
    :param title: Plot title
    :type title: str
    :param save_path: Path to save figure to.
    :type save_path: str
    :return: figure and axes for further customization
    :rtype: tuple    """

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct="%.0f%%")
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    if save_path:
        fig.savefig(save_path, bbox_inches='tight')
    return fig, ax


def create_bar_chart(values, labels, x_label='', y_label='', title='', horizontal=False, save_path=None):
    """
    Create a bar chart.
    :param values:
    :param labels:
    :param x_label: x axis label
    :type x_label: str
    :param y_label: y axis label
    :type y_label: str
    :param title: Plot title
    :type title: str
    :param save_path: Path to save figure to.
    :type save_path: str
    :return: figure and axes for further customization
    :rtype: tuple
    """

    fig, ax = plt.subplots()
    if not horizontal:
        ax.bar(values, labels)
        plt.xticks(rotation=90)  # Prevents long labels overlapping

    else:
        ax.barh(values, labels)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    fig.tight_layout()  # Prevents long labels being cutoff

    if save_path:
        fig.savefig(save_path, bbox_inches='tight')
    return fig, ax


if __name__ == '__main__':

    man_u = get_team_age_overall('Manchester United')
    man_c = get_team_age_overall('Manchester City')

    create_scatter_plot(man_u[0], man_u[1], 'Age', 'Overall', 'Manchester United Age vs Overall',
                        save_path='./figures/manu.png')
    create_scatter_plot(man_c[0], man_c[1], 'Age', 'Overall', 'Machester City Age vs Overall')

    position_counts = get_count_of_each_position()
    create_pie_chart(position_counts.values(), position_counts.keys())
    create_bar_chart(position_counts.keys(), position_counts.values(), y_label='Number', x_label='Position', title='Number of each position:')

    plt.show()
