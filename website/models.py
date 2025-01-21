from . import db
from flask_login import UserMixin
from sqlalchemy import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    contactinfo = db.Column(db.String(1000))
    offers = db.relationship('Offer')
    requests = db.relationship('Request')

class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10000))
    author = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    poster_id = db.Column(db.Integer)
    requester_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    offered_id = db.Column(db.Integer, db.ForeignKey('offer.id'))
    wanted_id = db.Column(db.Integer)
    
   
