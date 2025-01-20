from flask import Blueprint, render_template, request, redirect, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_data = request.form
        
    return render_template('login.html', user="hi")

@auth.route('/logout')
def logout():
    return "logs you out"

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
            flash("Account created successfully!", category='success')
        return render_template('signup.html', user="hi")
    else:
        return render_template('signup.html', user="hi")

