from flask import Flask, render_template, session, redirect, url_for, request, Blueprint
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, Column, Integer
import datetime

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "gaem.db")) # links to the database
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
'''
class Game(db.Model):
    gameid = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    name = db.Column(db.Text(80), unique=True, nullable=False, primary_key=False)
    dateadded = db.Column(db.DateTime, unique=False, nullable=False, primary_key=False)
    #useradded = db.Column(db.Text(80), unique=False, nullable=False, primary_key=False)
    description = db.Column(db.Text(80), unique=True, nullable=False, primary_key=False)
    datepublished = db.Column(db.DateTime, unique=False, nullable=False, primary_key=False)
    #publisher = db.Column(db.integer(80), unique=False, nullable=False, primary_key=False)
    #developer = db.Column(db.integer(80), unique=False, nullable=False, primary_key=False)
'''
@app.route('/')# home page
def home():
    return render_template('home.html')

@app.route('/index')# index for games
def index():
    #game = Game.query.all()
    games = session.query().all()
    for game in games:
        game_object = {'name': game.name,
                        'dateadded': game.dateadded,
                        'desciption': game.desciption,
                        'datepublished': game.datepublished}
        print(game_object)
    return render_template('home.html')


if __name__ == "__main__":
    app.run(debug=True)