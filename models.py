import os
from flask import Flask
from flask import g
from flask import session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///{}".format(os.path.join(os.path.dirname(os.path.abspath(__file__)), "kanban.db"))
app.secret_key = "cs162 is fun"

db = SQLAlchemy(app)

class Task(db.Model):
    __tablename__ = 'Task'

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False, primary_key=True)
    status = db.Column(db.String(32), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    
    def __repr__(self):
        return "<Title: {}>".format(self.title)

class User(UserMixin, db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    email = db.Column(db.String(200))
    password = db.Column(db.String(32))
    task_id = db.relationship('Task', backref='user', lazy='dynamic')
    
    def __repr__(self):
        return "<Username: {}>".format(self.username)

db.create_all()
db.session.commit()