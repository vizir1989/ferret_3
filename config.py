import os

SECRET_KEY = os.environ.get('SECRET_KEY',
                            'ueLB5KOP42EFeuIOsm50LklVrVO00br0E7C4t0d7eTpkEcmH/bhycdISwVHhPMZl1+aTQlsp2oqvVW3qgrN2/g==')
DATABASE = os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = False
