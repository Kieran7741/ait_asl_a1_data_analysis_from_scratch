"""
Sever a flask application that returns
a basic dash board for football team
"""


from flask import Flask, render_template, redirect,  send_file
from database.db import DB
from visualisation import visual
from utils.conversions import convert_money_string
import os

app = Flask(__name__, static_folder='./static_images/')

def generate_dashboard_resources(team):
    db = DB('database/players.db')

    result = db.select(['Overall'], where=f'Club="{team}"')
    average_overall = sum(result['Overall']) / float(len(result['Overall']))

    player_values =  db.select(['Value'], where=f'Club="{team}"')['Value']
    team_value = sum([convert_money_string(value) for value in player_values])
  
    image_path = f'static_images/{team}_age_v_overall.png'
    if not os.path.exists(image_path):
        result = db.select(['Age', 'Overall'], where=f'Club="{team}"')
        visual.create_scatter_plot(result['Age'], result['Overall'], title=f'{team} Age vs Overall',
                                   x_label='Age', y_label='Overall', plot_l_r_line=True, save_path=image_path)
    return average_overall, team_value

@app.route('/dashboard/<team>')
def dashboard(team):

    average_overall, team_value = generate_dashboard_resources(team)
    return 'success'
    # return render_template('dashboard.html', team=team, average_overall=average_overall)

@app.route('/')
def redirect_to_dashboard():
    return redirect("/dashboard/Arsenal")


if __name__=='__main__':
    app.run()
