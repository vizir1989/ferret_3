import os

SECRET_KEY = os.environ.get('SECRET_KEY',
                            'ueLB5KOP42EFeuIOsm50LklVrVO00br0E7C4t0d7eTpkEcmH/bhycdISwVHhPMZl1+aTQlsp2oqvVW3qgrN2/g==')
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///db.sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = False
