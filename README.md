# ferret_3

## What is this?

A system that provide 4 endpoints. 

* sign up

Register new user
```
    /user/signup?username=<username>&password=<password>
```

response: json with message and result

for example: {'message': 'enter the required fields', 'result': False}

* login

Check user name and password and return otp token
```
    /user/login?username=<username>&password=<password>
```

response: json with message and result

for example: {message=<totp_uri>, result=True}

* input token

Login
```
    /user/input_token?token=<token>
```

response: json with message and result plus cookie with jwt token

for example:  {message='login successfully', result=True}

* logout

Logout
```
    /user/logout
```

response: json with message and result

for example: {message='logout successfully', result=True}


## How to use

### docker

```
    docker build .
    docker-compose up
```

### curl

* signup
```
    curl -c cookies.txt -d 'username=user1&password=12345678' -X POST http://0.0.0.0:5000/user/signup
```

* login
```
    curl -c cookies.txt -d 'username=user1&password=12345678' -X POST http://0.0.0.0:5000/user/login
```

* input token
```
    curl -b cookies.txt -d 'token=34639875' -X POST http://0.0.0.0:5000/user/input_token
```

* logout
```
    curl -X GET http://0.0.0.0:5000/user/logout
```

### tox

How to run tox
```
    cd ./tests
    tox
```
