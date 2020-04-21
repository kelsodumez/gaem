from flask import Flask, render_template

app = Flask(__name__)

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