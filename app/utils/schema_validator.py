
from schema import Schema, And, Use, Optional, SchemaError
import re

class SchemaValidator:
    @staticmethod
    def validate_user(data):
        schema = Schema({
            'email': And(str, lambda s: '@' in s and len(s) <= 150),
            'password_hash': And(str, lambda s: len(s) > 0),
            'role': And(str, lambda s: s in ['sponsor', 'seeker', 'doer']),
            Optional('city'): str,
            Optional('phone'): And(str, lambda s: re.match(r'^\+?\d{9,15}$', s), error="Invalid phone number"),
            Optional('username'): And(str, lambda s: 3 <= len(s) <= 50 and s.isalnum(), error="Username must be 3-50 alphanumeric characters")
        })
        try:
            return schema.validate(data)
        except SchemaError as e:
            raise ValueError(f"Invalid input: {e}")

    @staticmethod
    def validate_username_update(data):
        schema = Schema({
            'username': And(str, lambda s: 3 <= len(s) <= 50 and s.isalnum(), error="Username must be 3-50 alphanumeric characters")
        })
        try:
            return schema.validate(data)
        except SchemaError as e:
            raise ValueError(f"Invalid input: {e}")