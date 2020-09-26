from marshmallow import Schema, fields
from marshmallow.validate import Length


class UserInputSchema(Schema):
    """ /user/login - POST
        /user/signup - POST

    Parameters:
     - username (str)
     - password (str)
    """

    username = fields.Str(required=True, validate=Length(min=4, max=64))
    password = fields.Str(required=True, validate=Length(min=4, max=64))