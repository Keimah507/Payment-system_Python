from typing import Any

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Float, Integer, Column
from sqlalchemy.orm import DeclarativeBase
from decimal import Decimal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


class Base(DeclarativeBase):
    pass


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(Integer, primary_key=True)
    username = db.Column(String(50), unique=True)
    email = db.Column(String(120), unique=True)
    password = db.Column(String(50), nullable=False, unique=True)
    wallet_id = db.Column(Integer, unique=True)
    wallet_balance = db.Column(Float)

    def __init__(self, username, email, password, wallet_balance, schema=None, **kw: Any):
        super().__init__(**kw)
        self.username = username
        self.password = password
        self.email = email
        self.wallet_balance = wallet_balance
        if schema:
            self.id = schema.get('id')
            self.wallet_id = schema.get(' wallet_id')

    def deposit(self, amount):
        self.wallet_balance += Decimal(amount)

    def withdraw(self, amount):
        if self.wallet_balance >= Decimal(amount):
            self.wallet_balance -= Decimal(amount)
        else:
            raise ValueError('Insufficient balance')



    def __repr__(self):
        return '<User {}>'.format(self.username)
