from flask import Flask
from flask_jsonrpc import JSONRPC

app = Flask(__name__)

rpc = JSONRPC(app, '/api', enable_web_browsable_api=True)

@rpc.method('tutorial.hello1(name=str)')
def hello1(name):
    return u'Hello, {0}!'.format2(name)

@rpc.method('tutorial.hello2(name=str)')
def hello2(name):
    class Object(object):
        pass

    return {
        'hello': name,
        'obj': Object()
    }

if __name__ == '__main__':
    import json

    app.debug = False
    with app.test_client() as client:
        print(client.post(
            '/api',
            data=json.dumps(dict(
                jsonrpc='2.0',
                method='tutorial.hello1',
                params=dict(name='jaru'),
                id='1'))).data)

    app.debug = True
    with app.test_client() as client:
        print(client.post(
            '/api',
            data=json.dumps(dict(
                jsonrpc='2.0',
                method='tutorial.hello1',
                params=dict(name='jaru'),
                id='1'))).data)

        print(client.post(
            '/api',
            data=json.dumps(dict(
                jsonrpc='2.0',
                method='tutorial.hello2',
                params=dict(name='jaru'),
                id='1'))).data)
