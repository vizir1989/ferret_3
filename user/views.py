import datetime

import jwt
from flask import jsonify, Blueprint, make_response, g, current_app
from flask import request, session
from flask_login import logout_user, current_user, login_user

from ferret import db, lm
from user.models import User

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route('/signup', methods=['POST'])
def signup():
    if current_user.is_authenticated:
        return jsonify(message='Logout before signup', result=False)

    try:
        username = request.form['username']
        password = request.form['password']
        if username and password:
            user = User.query.filter_by(username=username).first()
            if user is not None:
                return jsonify(message='username already exists.', result=False)
            # add new user to the database
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()

            session['username'] = user.username
            return jsonify(message='user created successfully', result=True)
        else:
            return jsonify(message='enter the required fields', result=False)
    except Exception as e:
        return jsonify(message=str(e), result=False)


@bp.route('/input_token', methods=['POST'])
def input_token():
    try:
        """User login route."""
        if not current_user.is_authenticated:
            # if user is logged in we get out of here
            return jsonify(message='login before input_token', result=False)

        if 'username' not in session:
            return jsonify(message='login before input token', result=False)

        user = User.query.filter_by(username=session['username']).first()
        if user is None:
            return jsonify(message='something wrong. Session user does not exist.', result=False)

        token = request.form['token']
        if user.verify_totp(token):
            resp = make_response(jsonify(message='login successfully', result=True))
            token = jwt.encode(
                {'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                current_app.config['SECRET_KEY'])
            resp.set_cookie('access_token', token)
            return resp
        else:
            return jsonify(message='invalid token', result=False)
    except Exception as e:
        return jsonify(message=str(e), result=False)


@bp.route('/login', methods=['POST'])
def login():
    """User login route."""
    if current_user.is_authenticated:
        # if user is logged in we get out of here
        return jsonify(message='logout before login', result=False)

    try:
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is None or not user.verify_password(password):
            return jsonify(message='Invalid username or password.', result=False)
        session['username'] = username
        login_user(user)
        return jsonify(message=user.get_totp_uri(), result=True)

    except Exception as e:
        return jsonify(message=str(e), result=False)


@bp.route('/logout')
def logout():
    """User logout route."""
    try:
        logout_user()
        return jsonify(message='logout successfully', result=True)
    except Exception as e:
        return jsonify(message=str(e), result=False)


@lm.user_loader
def load_user(user_id):
    """User loader callback for Flask-Login."""
    return User.query.get(int(user_id))
