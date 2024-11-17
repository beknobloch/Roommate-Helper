from flask_login import UserMixin
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Items(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    itemName = db.Column(db.String(200), nullable=False)
    itemPrice = db.Column(db.Float, nullable=False)
    payerID = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    paid = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Item %r>' % self.id


class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    balance = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    items = db.relationship('Items', secondary='user_items', backref='users')

    def __repr__(self):
        return '<User %r>' % self.id


user_items = db.Table(
    'user_items',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('item_id', db.Integer, db.ForeignKey('items.id'), primary_key=True),
)
