from flask import Flask
from flask_jsonrpc import JSONRPC

import json

app = Flask(__name__)
rpc = JSONRPC(app, '/api')


def check_auth(username, password):
    return username == 'USERNAME' and password == 'PASSWORD'

@rpc.method('tutorial.public_hello')
def public_hello():
    return u'Hello, World!'

@rpc.method('tutorial.private_hello(name=str)', authenticated=check_auth)
def private_hello(name):
    return u'Hello, {0}!'.format(name)

if __name__ == '__main__':
    with app.test_client() as client:
        print(client.post(
            '/api',
            data=json.dumps(dict(
                jsonrpc='2.0',
                method='tutorial.public_hello',
                params=dict(),
                id='1'))).data)

        print(client.post(
            '/api',
            data=json.dumps(dict(
                jsonrpc='2.0',
                method='tutorial.private_hello',
                params=dict(name='jaru'),
                id='1'))).data)

        print(client.post(
            '/api',
            data=json.dumps(dict(
                jsonrpc='2.0',
                method='tutorial.private_hello',
                params=dict(username='USERNAME', password='', name='jaru'),
                id='1'))).data)

        print(client.post(
            '/api',
            data=json.dumps(dict(
                jsonrpc='2.0',
                method='tutorial.private_hello',
                params=dict(username='USERNAME', password='PASSWORD', name='jaru'),
                id='1'))).data)

