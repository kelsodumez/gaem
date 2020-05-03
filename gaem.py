from flask import Flask, render_template, session, redirect, url_for, request
from markupsafe import escape

app = Flask(__name__)

app.secret_key = b'\x82\xc4\x0f\x8e\x02\x91q\xab|6-cy\xfct\x18'

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    return "login"
    
@app.route("/games")
def games():
    return "games"
if __name__ == "__main__":
    app.run(debug=True)