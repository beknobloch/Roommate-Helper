from flask_login import UserMixin
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserItem(db.Model):
    __tablename__ = 'user_items'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), primary_key=True)
    paid = db.Column(db.Boolean, default=False, nullable=False)

    # Relationships to access User and Item from UserItem
    user = db.relationship('Users', back_populates='user_items')
    item = db.relationship('Items', back_populates='user_items')

    def __repr__(self):
        return f'<UserItem user_id={self.user_id} item_id={self.item_id} paid={self.paid}>'

class Items(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    itemName = db.Column(db.String(200), nullable=False)
    itemPrice = db.Column(db.Float, nullable=False)
    payerID = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to UserItem
    user_items = db.relationship('UserItem', back_populates='item', cascade='all, delete-orphan')

    # To access users through the association
    users = db.relationship('Users', secondary='user_items', back_populates='items')

    def __repr__(self):
        return '<Item %r>' % self.id


class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    balance = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to UserItem
    user_items = db.relationship('UserItem', back_populates='user', cascade='all, delete-orphan')

    # To access items through the association
    items = db.relationship('Items', secondary='user_items', back_populates='users')

def __repr__(self):
        return '<User %r>' % self.id