from flask import Flask, render_template, session, redirect, url_for, request
from markupsafe import escape

app = Flask(__name__)#defines the app as a flask application

app.secret_key = b'\x82\xc4\x0f\x8e\x02\x91q\xab|6-cy\xfct\x18'#the secret key used for creating user specific sessions

login_manager = LoginManager()
login_manager.init_app(app)

@app.route("/")#this creates the homepage that users will default to when loading the site, unless they specify otherwise
def home():
    return render_template("home.html")

@app.route("/login")#login page
def login():
    return "login"
    
@app.route("/games")#this is the page that will be used to list all games in the database
def games():
    return "games"

if __name__ == "__main__":#the code that runs the website, debug=true makes it so that saving will auto update the site
    app.run(debug=True)