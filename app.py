"""
Sever a flask application that returns
a basic dashboard for football teams
"""


from flask import Flask, render_template, redirect, send_file, abort
from database.db import DB
from visualisation import visual
from utils.conversions import convert_money_string
from visualisation import stats
import os
import math

import matplotlib
# The Agg backend is used for as a non GUI backend.
# This is needed in order to make the use of matplotlib and flask thread safe
# See: https://stackoverflow.com/questions/49921721/runtimeerror-main-thread-is-not-in-main-loop-with-matplotlib-and-flask
matplotlib.use('Agg')


app = Flask(__name__, static_folder='./static_images/')


def generate_dashboard_resources(team):
    """
    Generate resources required for the team dashboard.

    Calculate average overall, total value of players and create
    :param team: Name of team
    :type team: str
    :return: Average team overall and total team value.
    :rtype: tuple
    """

    db = DB('database/players.db')

    result = db.select(['Overall', 'Value'], where=f'Club="{team}"')

    average_overall = stats.mean(result['Overall'])
    team_value = sum([convert_money_string(value) for value in result['Value']])
  
    image_path = f'static_images/{team}_age_v_overall.png'
    if not os.path.exists(image_path):
        result = db.select(['Age', 'Overall'], where=f'Club="{team}"')
        visual.create_scatter_plot(result['Age'], result['Overall'], title=f'{team} Age vs Overall',
                                   x_label='Age', y_label='Overall', plot_l_r_line=True, save_path=image_path)
    return average_overall, team_value


@app.route('/dashboard/<team>')
def dashboard(team):
    """
    Dashboard view function. Display a teams dashboard.
    :param team: Name of team
    :type team: str
    :return: flask.Response
    """

    # Validate team name
    db = DB('database/players.db')
    if db.validate_team(team):
        average_overall, team_value = generate_dashboard_resources(team)
        return render_template('dashboard.html', team=team, average_overall=math.ceil(average_overall),
                               team_value=team_value)
    else:
        return abort(404, f'Invalid team name: {team}')


@app.route('/overall_age/<team>')
def get_team_overall_age_image(team):
    """
    Return image of overall vs age plot for the provided team.
    :param team: Name of team to get image for.
    :type team: str
    :return: flask.Response containing image.
    :rtype: flask.Response
    """

    image_path = f'static_images/{team}_age_v_overall.png'
    if os.path.exists(image_path):
        return send_file(image_path, mimetype='image/png')
    else:
        return abort(404)


@app.route('/')
def redirect_to_dashboard():
    return redirect("/dashboard/Arsenal")


if __name__=='__main__':
    app.run()
