from flask import Flask, render_template, session, redirect, url_for, request, Blueprint, flash
from random import randint, choice
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, Column, Integer
import datetime
from werkzeug import generate_password_hash, check_password_hash

project_dir = os.path.dirname(os.path.abspath(__file__))
 # links to the database
database_file = "sqlite:///{}".format(os.path.join(project_dir, "gaem.db"))
app = Flask(__name__)
app.secret_key = ("29fc9d808e2fa590040dc20e43d41c7346324bf9fe184273")
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
'''
Below is all the classes needed to define data from the database
'''
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
    useradded = db.Column(db.ForeignKey('userinfo.username'))
    description = db.Column(db.Text, unique=True)
    datepublished = db.Column(db.Date)
    publisher = db.Column(db.ForeignKey('publishers.publishername'))
    developer = db.Column(db.ForeignKey('developers.developername'))
    developer1 = db.relationship('Developer', primaryjoin='Game.developer == Developer.developername', backref='games')
    publisher1 = db.relationship('Publisher', primaryjoin='Game.publisher == Publisher.publishername', backref='games')
    userinfo = db.relationship('Userinfo', primaryjoin='Game.useradded == Userinfo.username', backref='games')

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


def current_user(): # current user function
    if session.get("user"): # if it is able to get a session for user
        return Userinfo.query.get(session["user"]) # return the user info
    else:
        return False

'''
Below is all the routes for each webpage
'''

@app.route('/')  # home page
def home():
    return render_template('home.html', user=current_user())

@app.route('/login', methods=["GET","POST"]) # /login page
def login(): # login function
    if session.get("user"): # 
        return redirect('/') # redirects to home page
    if request.method == "POST": # request method 
        User = Userinfo.query.filter(Userinfo.username==request.form.get("username")).first() # form fillable to gain username variable
        if User and check_password_hash(User.password, request.form.get("password")): # checks to see if the password is correct
            flash("You logged in ya silly goose") # tells the user they have succesfully logged in
            return redirect('/') # redirects to home page
        else:
            flash(choice(["You're so smart you have an extra chromosome", "How many brain cells do you have? 1?", "you waste of oxygen!", "IDIOT", "that account doesnt exist"])) # error messages for failing to log in, hanan made me
            return redirect('/login') # redirects to login page
    return render_template("login.html") # the html template for this is login.html
    

@app.route('/logout') # /logout page
def logout(): # logout function
    try:
        session.pop("user") # ends user session
    except:
        print('you are already logged out!') # if there is no session to pop this will be printed
    return redirect("/login")

@app.route('/create', methods=["GET","POST"])
def create(): # create user function
    if request.method == "POST": 
            user_info = Userinfo (  
                username = request.form.get('username'), #  
                password = generate_password_hash(request.form.get('password'), salt_length=10),   
                isadmin = 0
            )
            db.session.add(user_info)
            db.session.commit()
    return render_template('create.html')

@app.route('/index')  # index for games
def index():
    game=None
    game=Game.query.all()
    return render_template('index.html', game=game)

@app.route('/game/<int:id>') # app route
def videogame(id):
    print(id)
    game=None
    game=Game.query.filter(Game.ID == id)
    return render_template('game.html', game=game)

app.route("/video")(lambda: "Hello World")

if __name__ == "__main__": 
    app.run(debug=True) # this runs the site site with debug active