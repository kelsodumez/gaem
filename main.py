from flask import Flask, render_template, session, redirect, url_for, request, Blueprint
import os
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

@app.route('/')#home page
def index():
    return render_template('index.html')

@app.route('/profile')#profile page
def profile():
    return render_template('profile.html')