from flask import Flask, render_template, session, redirect, url_for, request, Blueprint
import os
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "gaem.db")) # links to the database
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class game(db.Model):
    name = db.Column(db.Text(80), unique=True, nullable=False, primary_key=False)
    dateadded = db.Column(db.Date, unique=False, nullable=False, primary_key=False)
    #useradded = db.Column(db.Text(80), unique=False, nullable=False, primary_key=False)
    description = db.Column(db.Text(80), unique=True, nullable=False, primary_key=False)
    datepublished = db.Column(db.Date, unique=False, nullable=False, primary_key=False)
    #publisher = db.Column(db.integer(80), unique=False, nullable=False, primary_key=False)
    #developer = db.Column(db.integer(80), unique=False, nullable=False, primary_key=False)

@app.route('/')# home page
def home():
    return render_template('home.html')

@app.route('/index')# index for games
def index():
    game = game.query.all()
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)