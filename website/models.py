from . import db
from flask_login import UserMixin
from sqlalchemy import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    offers = db.relationship('Offer')

class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookname = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))

