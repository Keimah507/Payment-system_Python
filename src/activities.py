from temporalio import activity
from flask import Flask, request, jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import Base, User
from app.schemas.schema import UserSchema

engine = create_engine("sqlite:///users.db", echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

user_schema = UserSchema()

app = Flask(__name__)


@activity.defn
async def deposit(self, user_id, amount):
    data = request.get_json()

    data = request.get_json()

    session = Session()
    user = session.query(User).get(user_id)

    if user is None:
        return jsonify({'error': "User not found"}), 404

    user_data = user_schema.load(request.json)
    user.balance += user_data('amount')
    session.commit()

    result = user_schema.dump(user)
    return jsonify({'message': "Deposit Successful", "balance": user.balance}), 200


@activity.defn
async def withdraw(self, user_id, amount):
    data = request.get_json()

    session = Session()
    user = session.query(User).get(user_id)

    if user is None:
        return jsonify({'Error': "User Not found"}), 400

    user_data = user_schema.load(request.json)

    if user.balance < user_data['amount']:
        return jsonify({'Error': "Insufficient balance"}), 400

    user.balance -= user_data['amount']
    session.commit()
    session.close()

    return jsonify({'message': "Withdrawal successful", 'balance': user.balance}), 200
