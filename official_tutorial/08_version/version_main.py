from flask import Flask
from flask_jsonrpc import JSONRPC
from flask_jsonrpc.site import JSONRPCSite

app = Flask(__name__)
rpc1 = JSONRPC(app, '/api/v1', site=JSONRPCSite(), enable_web_browsable_api=True)
rpc2 = JSONRPC(app, '/api/v2', site=JSONRPCSite(), enable_web_browsable_api=True)


@rpc1.method('tutorial.index')
@rpc2.method('tutorial.index')
def index():
    return u'Welcome! Flask-JSON RPC'


# FIXME: 버전 1 브라우저에서 표시 안 됨
@rpc1.method('tutorial.hello')
def hello():
    return u'Hello, World!'


@rpc2.method('tutorial.hello_target(name=str)')
def hello(name):
    return u'Hello, {0}'.format(name)


if __name__ == '__main__':
    app.run()
