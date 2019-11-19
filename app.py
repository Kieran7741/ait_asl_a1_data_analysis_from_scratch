"""
Sever a flask application that returns
a basic dash board for football team
"""


from flask import Flask, render_template, redirect,  send_file


app = Flask(__name__, static_folder='./static_images/')

@app.route('/dashboard/<team>')
def dashboard(team):
    return render_template('dashboard.html', team=team)

@app.route('/')
def redirect_to_dashboard():
    return redirect("/dashboard/Arsenal")


@app.route('/get_image/<image_name>')
def get_image(image_name):

    return send_file(f'static_images/{image_name}.png', mimetype='image/png')

if __name__=='__main__':
    app.run()
