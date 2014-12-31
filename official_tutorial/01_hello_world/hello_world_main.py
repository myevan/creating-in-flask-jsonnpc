from flask import Flask
from flask_jsonrpc import JSONRPC

import json

app = Flask(__name__)
rpc = JSONRPC(app, '/api')

@rpc.method('tutorial.hello')
def hello():
    return u'Hello, World!'


if __name__ == '__main__':
    with app.test_client() as client:
        print(client.post(
            '/api',
            data=json.dumps(dict(
                jsonrpc='2.0',
                method='tutorial.hello',
                params=dict(),
                id='1'))).data)
