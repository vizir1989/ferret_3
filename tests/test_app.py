import json

from pyotp import totp

username_1 = 'test'
password_1 = '12345678'
short_username = 'tes'
short_password = '123'


def login(client, username, password):
    return client.post('/user/login', data=dict(
        username=username,
        password=password
    ))


def logout(client):
    return client.get('/user/logout')


def sign_up(client, username, password):
    return client.post('/user/signup', data=dict(
        username=username,
        password=password
    ))


def input_token(client, token):
    return client.post('/user/input_token', data=dict(
        token=token
    ))


def test_login(client):
    rv = sign_up(client, username_1, password_1)
    response = json.loads(rv.data)
    assert response['result']
    rv = login(client, username_1, password_1)
    response = json.loads(rv.data)
    assert response['result']


def test_login_without_signup(client):
    rv = login(client, username_1, password_1)
    response = json.loads(rv.data)
    assert not response['result']


def test_login_twice(client):
    rv = sign_up(client, username_1, password_1)
    response = json.loads(rv.data)
    assert response['result']
    rv = login(client, username_1, password_1)
    response = json.loads(rv.data)
    assert response['result']
    rv = login(client, username_1, password_1)
    response = json.loads(rv.data)
    assert not response['result']


def test_input_token_without_login(client):
    rv = sign_up(client, username_1, password_1)
    response = json.loads(rv.data)
    assert response['result']
    rv = input_token(client, '12345678')
    response = json.loads(rv.data)
    assert not response['result']


def test_input_wrong_token(client):
    rv = sign_up(client, username_1, password_1)
    response = json.loads(rv.data)
    assert response['result']
    rv = login(client, username_1, password_1)
    response = json.loads(rv.data)
    assert response['result']
    rv = input_token(client, '12345678')
    response = json.loads(rv.data)
    assert not response['result']


def test_input_token(client):
    rv = sign_up(client, username_1, password_1)
    response = json.loads(rv.data)
    assert response['result']
    rv = login(client, username_1, password_1)
    response = json.loads(rv.data)
    assert response['result']
    from urllib.parse import urlparse, parse_qs
    parsed = urlparse(response['message'])
    parsed_query = parse_qs(parsed.query)
    digits = int(parsed_query['digits'][0])
    period = int(parsed_query['period'][0])
    secret = parsed_query['secret'][0]
    token = totp.TOTP(secret, interval=period, digits=digits).now()
    rv = input_token(client, str(token))
    response = json.loads(rv.data)
    assert response['result']


def test_shor_name(client):
    rv = sign_up(client, short_username, password_1)
    response = json.loads(rv.data)
    assert not response['result']


def test_shor_password(client):
    rv = sign_up(client, username_1, short_password)
    response = json.loads(rv.data)
    assert not response['result']
