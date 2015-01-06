from flask import Flask
from flask import g, current_app

from flask_jsonrpc import JSONRPC
from flask_jsonrpc.exceptions import InvalidParamsError, InvalidCredentialsError

from itsdangerous import TimedJSONWebSignatureSerializer as TokenSerializer
from itsdangerous import SignatureExpired, BadSignature

from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'TEMP_SECRET_KEY'

# using https://github.com/myevan/flask-jsonrpc
app.config['JSONRPC_AUTH_ARGUMENT_NAMES'] = ['token']
app.config['JSONRPC_AUTH_ARGUMENT_TYPES'] = ['String']

app.config['JSONRPC_AUTH_TOKEN_DURATION'] = 1

USER_TABLE = {
    0: {
        'username': 'myevan',
        'password': 'PASSWORD',
        'full_name': 'Song Young-Jin',
    }
}


def authenticate(f, f_parse_auth_token):
    @wraps(f)
    def _f(*args, **kwargs):
        try:
            creds = args[:1]
            auth_dict = f_parse_auth_token(creds[0])
            if auth_dict is None:
                raise InvalidCredentialsError()
            else:
                args = args[1:]
        except IndexError:
            if 'auth_token' in kwargs:
                auth_dict = f_parse_auth_token(kwargs['auth_token'])
                if auth_dict is None:
                    raise InvalidCredentialsError()
                else:
                    kwargs.pop('auth_token')
            else:
                raise InvalidParamsError(
                    'Authenticated methods require'
                    'at least [{0}] or {{{0}:}} arguments'.format('auth_token'))

        g.user_id = auth_dict['user_id']
        return f(*args, **kwargs)
    return _f


def parse_auth_token(token):
    token_serializer = TokenSerializer(app.config['SECRET_KEY'])

    try:
        return token_serializer.loads(token)
    except SignatureExpired:
        return None
    except BadSignature:
        return None


rpc = JSONRPC(app, '/api', auth_backend=authenticate)


@rpc.method('tutorial.public_login(username=str, password=str)')
def public_login(username, password):
    user_id = None
    user_dict = None
    for each_user_id, each_user_dict in USER_TABLE.items():
        if each_user_dict['username'] == username:
            user_id = each_user_id
            user_dict = each_user_dict
            break
    else:
        raise ValueError('WRONG_AUTH_INFO')

    if user_dict['password'] != password:
        raise ValueError('WRONG_AUTH_INFO')

    token_serializer = TokenSerializer(
        app.config['SECRET_KEY'],
        expires_in=app.config['JSONRPC_AUTH_TOKEN_DURATION'])

    return {
        'auth_token': token_serializer.dumps(dict(user_id=user_id))
    }


@rpc.method('tutorial.public_hello')
def public_hello():
    return u'Hello, World!'


@rpc.method('tutorial.private_hello(name=str)', authenticated=parse_auth_token)
def private_hello():
    user_dict = USER_TABLE.get(g.user_id)
    return u'Hello, {0}!'.format(user_dict['full_name'])


if __name__ == '__main__':
    import json

    app.debug = True

    with app.test_client() as client:
        print(client.post(
            '/api',
            data=json.dumps(dict(
                jsonrpc='2.0',
                method='tutorial.public_hello',
                params=dict(),
                id='1'))).data)

        login_dict = json.loads(client.post(
            '/api',
            data=json.dumps(dict(
                jsonrpc='2.0',
                method='tutorial.public_login',
                params=dict(username='myevan', password='PASSWORD'),
                id='2'))).data)

        print login_dict
        auth_token = login_dict['result']['auth_token']
        print(client.post(
            '/api',
            data=json.dumps(dict(
                jsonrpc='2.0',
                method='tutorial.private_hello',
                params=dict(auth_token=auth_token),
                id='1'))).data)
