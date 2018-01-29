from sqlalchemy import ForeignKey
from sqlalchemy.orm import backref

from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(320), unique=True)
    password = db.Column(db.String(32), nullable=False)
    logincount = db.Column(db.Integer)
    articles = db.relationship('Article', lazy="dynamic")
    def __repr__(self):
        return '<User %r>' % self.username

class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text)
    author = db.Column(db.String(80))
    commit_time = db.Column(db.DateTime)
    edit_time = db.Column(db.DateTime)
    tag = db.Column(db.String(80))
    view_count = db.Column(db.Integer)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    def __repr__(self):
        return '<Article %r>' % self.title

# class Admin(db.Model):
#     __tablename__ = 'admins'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True)
#     email = db.Column(db.String(320), unique=True)
#     password = db.Column(db.String(32), nullable=False)
#
#     def __repr__(self):
#         return '<User %r>' % self.username