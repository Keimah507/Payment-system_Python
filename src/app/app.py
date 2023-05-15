from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from temporalio import workflow, activity

with workflow.unsafe.imports_passed_through():
    from workflows import DepositWorkflow, WithdrawWorkflow


from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User, app, db
from schemas.schema import UserSchema


engine = create_engine("sqlite:///users.db", echo=True)
with app.app_context():
    db.create_all()

Session = sessionmaker(bind=engine)

user_schema = UserSchema()


@app.route('/create_account', methods=['POST'])
def register():
    """
    Creates account using SQLAlchemy model
    """
    data = request.get_json()
    # create new user
    user = User(
        username=data['username'],
        email=data['email'],
        password=generate_password_hash(data["password"], method='sha256'),
    )

    errors = user_schema.validate(user_schema.dump(user))
    if errors:
        return jsonify(errors), 400

    try:
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return jsonify({'id': user.id, 'username': user.username, 'email': user.email}), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 409
    finally:
        db.session.close()


@activity.defn
@app.route('/deposit/<int:user_id>', methods=['POST'])
async def deposit_funds(user_id):
    """
    Deposits fund into wallet
    """
    data = request.get_json()
    amount = data.get('amount')

    user = User.query.filter(User.id == user_id).first()

    if user is None:
        return jsonify({'error': "User not found"}), 404

    try:
        await User.deposit(amount)
        db.session.commit()
        return jsonify({'message': "Deposit Successful", "balance": user.wallet_balance}), 200
    except ValueError as e:
        return jsonify({'Error': str(e)}), 400


@activity.defn
@app.route('/withdraw/<int:user_id>', methods=['POST'])
async def withdraw_funds(user_id):
    """
    Withdraws from app wallet
    """
    data = request.get_json()
    amount = data.get('amount')

    user = User.query.filter(User.id == user_id).first()

    if user is None:
        return jsonify({'Error': "User Not found"}), 400

    # user_data = user_schema.load(request.json)
    #
    # if user.balance < data['amount']:
    #     return jsonify({'Error': "Insufficient balance"}), 400
    #
    # user.balance -= data['amount']
    try:
        await WithdrawWorkflow.withdraw_funds(amount)
        db.session.commit()
        db.session.close()
        return jsonify({'message': "Withdrawal successful", 'balance': user.wallet_balance}), 200
    except ValueError as e:
        return jsonify({'Error': str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
