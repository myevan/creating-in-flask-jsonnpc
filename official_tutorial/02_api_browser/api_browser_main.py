from flask import Flask
from flask_jsonrpc import JSONRPC

app = Flask(__name__)
rpc = JSONRPC(app, '/api', enable_web_browsable_api=True)

@rpc.method('tutorial.hello(name=str)')
def hello(name):
    return u'Hello, {0}!'.format(name)


if __name__ == '__main__':
    app.run()
