from marshmallow import Schema, fields


class UserSchema(Schema):

    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    wallet_id = fields.Int(dump_only=True)
    wallet_balance = fields.Float(dump_only=True, default=0)