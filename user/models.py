import base64
import os
from datetime import datetime, timedelta

from flask import current_app
from flask_login import UserMixin
from pyotp import totp
from werkzeug.security import generate_password_hash, check_password_hash

from ferret import db


class User(UserMixin, db.Model):
    """User model."""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))
    otp_secret = db.Column(db.String(16))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.otp_secret is None:
            # generate a random secret
            self.otp_secret = base64.b32encode(os.urandom(10)).decode('utf-8')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_totp_uri(self):
        totp_uri = totp.TOTP(self.otp_secret, interval=300, digits=8).provisioning_uri(self.username, issuer_name="Ferret")
        return totp_uri

    def verify_totp(self, token):
        return totp.TOTP(self.otp_secret, interval=300, digits=8).verify(token)
