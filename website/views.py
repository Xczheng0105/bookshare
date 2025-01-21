from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user
from .models import Offer
from .models import db
from sqlalchemy import text

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        id = request.form.get("id")
        return redirect(url_for('views.info', id=id))
    else:
        rows = db.session.execute(text('SELECT offer.id, offer.title, offer.author, user.username FROM offer JOIN user ON user.id=offer.userid WHERE offer.userid != :uid'), {'uid': current_user.id})
        return render_template("index.html", user=current_user, rows=rows)

@views.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        # Add the offer
        title = request.form.get('title')
        author = request.form.get('author')
        userid = current_user.id

        if not title:
            flash("Title cannot be empty!", category='error')
            return redirect(url_for("views.add"))
        elif not author:
            flash("Author cannot be empty!", category='error')
            return redirect(url_for("views.add"))

        new_offer = Offer(title=title, author=author, userid=userid)
        db.session.add(new_offer)
        db.session.commit()
        flash("Offer added successfully!", category='success')

        # Redirect back to homepage
        return redirect(url_for("views.home"))
    else:
        return render_template("add.html", user=current_user)
    
@views.route('/info', methods=['GET'])
@login_required
def info():
    oid = int(request.args.get('id'))
    query = db.session.execute(text('SELECT offer.title, offer.author, user.username, user.contactinfo FROM offer JOIN user ON user.id=offer.userid WHERE offer.id = :oid'), {'oid': oid}).first()
    return render_template("info.html", user=current_user, query=query)

