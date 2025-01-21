from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user
from .models import Offer, Request
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
    
@views.route('/myoffers', methods=['GET', 'POST'])
@login_required
def myoffers():
    if request.method == 'POST':
        id = request.form.get("id")
        return redirect(url_for('views.myoffersinfo', id=id))
    else:
        rows = db.session.execute(text('SELECT id, title, author FROM offer WHERE userid = :uid'), {'uid': current_user.id})
        return render_template("myoffers.html", rows=rows, user=current_user)
    
@views.route('/info', methods=['GET', 'POST'])
@login_required
def info():
    if request.method == 'POST':
        id = int(request.args.get("id"))
        return redirect(url_for('views.exchange', id=id))
    else:
        id = int(request.args.get("id"))
        query = db.session.execute(text('SELECT * FROM offer JOIN user ON user.id=offer.userid WHERE offer.id = :id'), {'id':id}).first()
        return render_template("info.html", user=current_user, query=query)

@views.route('/myoffersinfo', methods=['GET', 'POST'])
@login_required
def myoffersinfo():
    if request.method == 'POST':
        # Deletion of a user's own offer
        id = request.form.get("id")
        print(id)
        db.session.execute(text('DELETE FROM offer WHERE id = :id'), {'id': id})
        db.session.commit()
        return redirect(url_for('views.myoffers'))
    else:
        oid = int(request.args.get('id'))
        query = db.session.execute(text('SELECT id, title, author, date FROM offer WHERE id = :oid'), {'oid': oid}).first()
        return render_template("myoffersinfo.html", user=current_user, query=query)
    
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
    
@views.route('/exchange', methods=['GET', 'POST'])
@login_required
def exchange():
    if request.method == 'POST':
        wid = int(request.args.get("id"))
        offered_title = request.form.get("offered_title")
        if not offered_title:
            flash("You need to choose something to exchange!", category='error')
            return redirect(url_for('views.exchange', id=wid))
        
        pid = request.form.get("poster_id")
        rid = current_user.id
        oid = request.form.get("offered_id")
        wid = int(request.args.get("id"))
        
        new_request = Request(poster_id=pid, requester_id=rid, offered_id=oid, wanted_id=wid)
        db.session.add(new_request)
        db.session.commit()
        return redirect("/")
    else:
        id = int(request.args.get("id"))
        offer = db.session.execute(text('SELECT * FROM offer JOIN user ON user.id = offer.userid WHERE offer.id = :id'), {'id': id}).first()
        avail = db.session.execute(text('SELECT * FROM offer WHERE userid = :id'), {'id': current_user.id})
        return render_template("exchange.html", user=current_user, avail=avail, offer=offer)

@views.route('/requests', methods=['GET', 'POST'])
@login_required
def requests():
    if request.method == 'POST':
        id = request.form.get("row_id")
        return redirect(url_for('views.requestinfo', id=id))
    else:
        rows = db.session.execute(text('SELECT request.id, request.date, user.username, offer.title, offer.author FROM request JOIN user ON request.requester_id=user.id JOIN offer ON request.wanted_id=offer.id WHERE poster_id=:id'),
                                  {'id': current_user.id})
        return render_template("requests.html", rows=rows, user=current_user)
    
@views.route('/requestinfo', methods=['GET', 'POST'])
@login_required
def requestinfo():
    id = int(request.args.get("id"))
    req = db.session.execute(text('SELECT * FROM request WHERE id=:id'), {'id': id}).first()
    wanted_title = db.session.execute(text('SELECT title FROM offer WHERE id = :id'), {'id': req.wanted_id}).first().title
    wanted_author = db.session.execute(text('SELECT author FROM offer WHERE id = :id'), {'id': req.wanted_id}).first().author
    offered_title = db.session.execute(text('SELECT title FROM offer WHERE id = :id'), {'id': req.offered_id}).first().title
    offered_author = db.session.execute(text('SELECT author FROM offer WHERE id = :id'), {'id': req.offered_id}).first().author
    requester = db.session.execute(text('SELECT username FROM user WHERE id = :id'), {'id': req.requester_id}).first().username
    
    if request.method == 'POST':
        db.session.execute(text('DELETE FROM offer WHERE id=:id'), {'id': req.wanted_id})
        db.session.execute(text('DELETE FROM offer WHERE id=:id'), {'id': req.offered_id})
        db.session.execute(text('DELETE FROM request WHERE wanted_id=:id'), {'id': req.wanted_id})
        db.session.execute(text('DELETE FROM request WHERE offered_id=:id'), {'id': req.offered_id})
        db.session.commit()
        return redirect(url_for('views.requests'))
    else:
        return render_template("requestinfo.html", 
                            req=req, 
                            offered_title=offered_title, 
                            wanted_title=wanted_title, 
                            wanted_author=wanted_author,
                            offered_author=offered_author,
                            requester=requester, 
                            user=current_user
                            )

