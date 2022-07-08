from argparse import OPTIONAL
from pkg_resources import require
from sqlalchemy import null
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class AskedQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(60))
    body = db.Column(db.String(2000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    image1 = db.Column(db.String())
    image2 = db.Column(db.String())
    image3 = db.Column(db.String())
    answer = db.Column(db.String(2000))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class SavedQuestion():
    pass


class Tutorial():
    pass


class SavedTutorial():
    pass


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    asked_questions = db.relationship('AskedQuestion')
