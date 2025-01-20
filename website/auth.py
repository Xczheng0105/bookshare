from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return "login page"

@auth.route('/logout')
def logout():
    return "logs you out"

@auth.route('/signup')
def signup():
    return "signup page"

