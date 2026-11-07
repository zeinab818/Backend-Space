from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.String()
    name = fields.String()
    email = fields.String()