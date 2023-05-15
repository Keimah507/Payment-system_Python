import uuid

from marshmallow import Schema, fields


class UserSchema(Schema):

    id = fields.Int(allow_none=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True, nullable=False)
    password = fields.Str(required=True, nullable=False)
    wallet_id = fields.Str(default=str(uuid.uuid4()), allow_none=True)
    wallet_balance = fields.Float(default=0, as_string=True, allow_none=True)
