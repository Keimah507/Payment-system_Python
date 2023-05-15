import uuid
from dataclasses import dataclass
from typing import Any

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from decimal import Decimal


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


class Base(DeclarativeBase):
    pass


@dataclass
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(String(50), unique=True)
    email = db.Column(String(120), unique=True)
    password = db.Column(String(50), nullable=False, unique=True)
    wallet_id = db.Column(String(36), default=str(uuid.uuid4()))
    wallet_balance = db.Column(db.Numeric(precision=10, scale=2), default=0)

    # @classmethod
    # def __init__(self, username, email, password, schema=None, **kw: Any):
    #     super().__init__(**kw)
    #     self.username = username
    #     self.password = password
    #     self.email = email
    #     if schema:
    #         self.id = schema.get('id')
    #         self.wallet_id = schema.get(' wallet_id')
    #         self.wallet_balance = schema.get('wallet_balance')

    @classmethod
    def deposit(self, amount):
        self.wallet_balance += Decimal(amount)

    @classmethod
    def withdraw(self, amount):
        if self.wallet_balance >= Decimal(amount):
            self.wallet_balance -= Decimal(amount)
        else:
            raise ValueError('Insufficient balance')

    @classmethod
    def __repr__(self):
        return '<User {}>'.format(self.username)
