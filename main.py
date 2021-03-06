from flask import Flask, render_template, session, redirect, url_for, request, Blueprint, flash
from random import randint, choice
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, Column, Integer
#from werkzeug import generate_password_hash, check_password_hash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

project_dir = os.path.dirname(os.path.abspath(__file__))
 # links to the database
database_file = "sqlite:///{}".format(os.path.join(project_dir, "gaem.db"))
app = Flask(__name__)
app.secret_key = ("29fc9d808e2fa590040dc20e43d41c7346324bf9fe184273") # secret key for user password salting & hashing
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app) # defines 'db' as the sqlalchemy connection
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

class Game(db.Model):
    __tablename__ = 'games'
    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)
    dateadded = db.Column(db.Date)#Date)
    useradded = db.Column(db.ForeignKey('userinfo.username'))
    description = db.Column(db.Text, unique=True)
    datepublished = db.Column(db.Text)#Date)
    publisher = db.Column(db.ForeignKey('publishers.publishername'))
    developer = db.Column(db.ForeignKey('developers.developername'))
    developer1 = db.relationship('Developer', primaryjoin='Game.developer == Developer.developername', backref='games')
    publisher1 = db.relationship('Publisher', primaryjoin='Game.publisher == Publisher.publishername', backref='games')
    userinfo = db.relationship('Userinfo', primaryjoin='Game.useradded == Userinfo.username', backref='games')

class Publisher(db.Model):
    __tablename__ = 'publishers'
    ID = db.Column(db.Integer, primary_key=True)
    publishername = db.Column(db.Text)

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

@app.context_processor
def add_current_user():
    if session.get('user'): # if a user is logged in
        return dict(current_user=Userinfo.query.get(session['user'])) # current user is equal to userinfo of user session
    return dict(current_user=None) # otherwise current user is none

#@app.route('/')  # home page
#def home():
    #return render_template('home.html', user=current_user())

@app.route('/login', methods=["GET","POST"]) # /login page
def login(): # login function
    if session.get("user"): # 
        return redirect('/') # redirects to home page
    if request.method == "POST": # request method 
        User = Userinfo.query.filter(Userinfo.username==request.form.get("username")).first() # form fillable to gain username variable:
        if User and check_password_hash(User.password, request.form.get("password")): # checks to see if the password is correct
            flash("You have succesfully logged in") # tells the user they have succesfully logged in.
            session['user']=User.ID
            return redirect('/') # redirects to home page
        else:
            return render_template('login.html', error='Username exceeds limit of 20 characters or does not exist')
    return render_template("login.html") # the html template for this is login.html
    

@app.route('/logout') # /logout page
def logout(): # logout function
    try:
        session.pop("user") # ends user session
    except:
        print('you are already logged out!') # if there is no session to pop this will be printed
        return redirect("/login")
    return redirect("/")

@app.route('/create', methods=["GET","POST"])
def create(): # create user function
    if request.method == "POST":
        if len(request.form.get('username')) > 20: # if the inputted username is greater than 20 characters it will not be accepted
            return render_template('create.html', error='Username exceeds limit of 20 characters') # prompts the user to create a shorter username
        elif Userinfo.query.filter(Userinfo.username == request.form.get("username")).first():
            return render_template('create.html', error='Username already in use') # prompts the user to create a unique username
        else:
            user_info = Userinfo (  
                username = request.form.get('username'), # requests username from the user as a form
                password = generate_password_hash(request.form.get('password'), salt_length=10), # requests password from the user as a form then salts and hashes it with a salt length of 10
                isadmin = 0 # user account is not an admin
            )
            db.session.add(user_info) # adds the data to the database
            db.session.commit() # commits the add
    return render_template('create.html')

@app.route('/delete', methods=["POST"])
def delete():
    if current_user() == False:
        return render_template('index.html', error='To delete a comment you must be logged in as the creator of the comment or an admin')
    elif current_user().ID == int(request.form["userid"]): # if the id of the user logged in is equal to the id of the user that added the comment 
        deletion_ID = request.form["deletion"] # requests form input for what to delete from html
        to_delete = Comment.query.get(deletion_ID) # queries comment table based on form input to find data to delete
        db.session.delete(to_delete) # deletes to_delete
        db.session.commit() # commits changes
    elif current_user().ID == 1: # id of admin is 1
        deletion_ID = request.form["deletion"]
        to_delete = Comment.query.get(deletion_ID)
        db.session.delete(to_delete)
        db.session.commit()
    print(request.full_path)
    return redirect(request.form.get('from','/'))

@app.route('/')  # index for games
def index():
    game=Game.query.all() # queries the database for data from the table
    return render_template('index.html', game=game) # returns the queried data as 'game'

@app.route('/game/<int:id>') # app route
def videogame(id):
    #print(id) # prints the id (for debug)
    game=Game.query.get(id) # queries the database for data from the table where the id of the data is equal to the id of the game selected
    return render_template('game.html', game=game) # returns the queried data as 'game'

@app.route('/comment/<int:id>', methods=["POST"])
def comment(id):
    #print(id) # debug
    #print(request.full_path) # more debug
    user = current_user()
    if user: # user data/inputs from the html section are defined into their respective rows of the comment table
        new_comment = Comment() # new_comment is to be added to the comments table
        new_comment.userinfo = current_user() #user info is equal to the current user
        new_comment.game = Game.query.get(id) #the game id is gained from the form
        new_comment.comment = request.form.get('comment') # the comment is gained from the form
        print(new_comment.userinfo) # debug
        if request.form.get('comment'): # if the comment form is submitted
            print("here") #debug
            db.session.add(new_comment) # adds the comment to the db
            db.session.commit() # commits the change
    return redirect(request.form.get('from', '/'))

@app.route('/creategame', methods=["POST"])
def creategame():
    user=current_user()
    if user: # if there is a user logged in
        new_game = Game()
        new_game.name = request.form.get('gamename') # the name of the game to be added is gained from the form
        new_game.dateadded = datetime.utcnow() # the date added is taken from the datetime function to gain the time of submission
        new_game.userinfo = current_user() # userinfo is equal to the current user logged in
        new_game.description = request.form.get('description') # gained from form
        new_game.datepublished = str(request.form.get('datepublished')) # gained from form as a string
        new_game.publisher = request.form.get('publisher') # gained from form
        new_game.developer = request.form.get('developer') # gained from form
        print(new_game.name, '''new_game.dateadded,''', new_game.useradded, new_game.description, new_game.datepublished, 
        new_game.publisher, new_game.developer) # debug
        if request.form.get('gamename'):
            print(new_game.name, '''new_game.dateadded,''', new_game.useradded, new_game.description, new_game.datepublished, 
            new_game.publisher, new_game.developer) # debug
            print("here the second") # debug
            db.session.add(new_game)
            db.session.commit() # this probably isnt working because of publisher & developer being foreign keys, need to figure out how to get around this
    return redirect(request.form.get('from', '/')) # redirects to index

if __name__ == "__main__": 
    app.run(debug=True) # this runs the site site with debug active