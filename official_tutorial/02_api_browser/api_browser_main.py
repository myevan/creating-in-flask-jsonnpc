from flask import Flask
from flask_jsonrpc import JSONRPC

import json

app = Flask(__name__)
rpc = JSONRPC(app, '/api', enable_web_browsable_api=True)

@rpc.method('tutorial.hello')
def hello():
    return u'Hello, World!'


if __name__ == '__main__':
    app.run()
