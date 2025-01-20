from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home')) 
        flash("Incorrect username/password!", category='error')
        
    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        passwordC = request.form.get('passwordC')

        if len(username) == 0:
            flash("Username should not be empty!", category='error')
        elif len(password) == 0:
            flash("Password cannot be empty!", category='error')
        elif password != passwordC:
            flash("Passwords do not match!", category='error')
        else:         
            new_user = User(username=username, password=generate_password_hash(password, method='scrypt'))
            try:
                db.session.add(new_user)
                db.session.commit()
                flash("Account created successfully!", category='success')
                return redirect("/login")
            except:
                flash("Username already exists!", category='error')
                
        return render_template('signup.html', user="hi")         
    else:
        return render_template('signup.html', user="hi")

