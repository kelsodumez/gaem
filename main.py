from flask import Flask, render_template, session, redirect, url_for, request, Blueprint
from markupsafe import escape
from . import db

main = Blueprint('main', __name__)

@main.route('/')#home page
def index():
    return 'Index'

@main.route('/profile')#profile page
def profile():
    return 'Profile'