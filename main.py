from flask import Flask, render_template, session, redirect, url_for, request, Blueprint
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, Column, Integer
import datetime

project_dir = os.path.dirname(os.path.abspath(__file__))
 # links to the database
database_file = "sqlite:///{}".format(os.path.join(project_dir, "gaem.db"))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Comment(db.Model):
    __tablename__ = 'comments'

    ID = db.Column(db.Integer, primary_key=True)
    gameid = db.Column(db.ForeignKey('games.ID'))
    userid = db.Column(db.ForeignKey('userinfo.ID'))
    comment = db.Column(db.Text)

    game = db.relationship('Game', primaryjoin='Comment.gameid == Game.ID', backref='comments')
    userinfo = db.relationship('Userinfo', primaryjoin='Comment.userid == Userinfo.ID', backref='comments')



class Developer(db.Model):
    __tablename__ = 'developers'

    ID = db.Column(db.Integer, primary_key=True)
    developername = db.Column(db.Text)



class Gamegenre(db.Model):
    __tablename__ = 'gamegenre'

    ID = db.Column(db.Integer, primary_key=True)
    gameid = db.Column(db.ForeignKey('games.ID'))
    genreid = db.Column(db.Integer)

    game = db.relationship('Game', primaryjoin='Gamegenre.gameid == Game.ID', backref='gamegenres')


class Genre(Gamegenre):
    __tablename__ = 'genres'

    ID = db.Column(db.ForeignKey('gamegenre.ID'), primary_key=True)
    genrename = db.Column(db.Text)
    description = db.Column(db.Text)



class Game(db.Model):
    __tablename__ = 'games'

    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)
    dateadded = db.Column(db.Date)
    useradded = db.Column(db.ForeignKey('userinfo.ID'))
    description = db.Column(db.Text, unique=True)
    datepublished = db.Column(db.Date)
    publisher = db.Column(db.ForeignKey('publishers.ID'))
    developer = db.Column(db.ForeignKey('developers.ID'))

    developer1 = db.relationship('Developer', primaryjoin='Game.developer == Developer.ID', backref='games')
    publisher1 = db.relationship('Publisher', primaryjoin='Game.publisher == Publisher.ID', backref='games')
    userinfo = db.relationship('Userinfo', primaryjoin='Game.useradded == Userinfo.ID', backref='games')



class Publisher(db.Model):
    __tablename__ = 'publishers'

    ID = db.Column(db.Integer, primary_key=True)
    publishername = db.Column(db.Text)



class Rating(db.Model):
    __tablename__ = 'ratings'

    ID = db.Column(db.Integer, primary_key=True)
    gameid = db.Column(db.ForeignKey('games.ID'))
    userid = db.Column(db.ForeignKey('userinfo.ID'))
    rating = db.Column(db.Integer)

    game = db.relationship('Game', primaryjoin='Rating.gameid == Game.ID', backref='ratings')
    userinfo = db.relationship('Userinfo', primaryjoin='Rating.userid == Userinfo.ID', backref='ratings')



class Userinfo(db.Model):
    __tablename__ = 'userinfo'

    ID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    isadmin = db.Column(db.Boolean)


@app.route('/')  # home page
def home():
    return render_template('home.html')


@app.route('/index')  # index for games
def index():
    game=None
    game=Game.query.all()
    return render_template('index.html', game=game)

if __name__ == "__main__":
    app.run(debug=True)
