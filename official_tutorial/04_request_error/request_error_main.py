from flask import Flask
from flask_jsonrpc import JSONRPC

app = Flask(__name__)
app.debug = True

rpc = JSONRPC(app, '/api', enable_web_browsable_api=True)

@rpc.method('tutorial.hello(name=str)')
def hello(name):
    app.logger.debug('tutorial.hello:{0}'.format(name))
    return u'Hello, {0}!'.format(name)


if __name__ == '__main__':
    import json

    with app.test_client() as client:
        print(client.post(
            '/api',
            data=json.dumps(dict(
            ))).data)

        print(client.post(
            '/api',
            data=json.dumps(dict(
                method='tutorial.hello',
                params=dict(name='jaru')
            ))).data)

        print(client.post(
            '/api',
            data=json.dumps(dict(
                jsonrpc='2.0',
                method='tutorial.hello',
                params=dict(),
                id='1'))).data)

        print(client.post(
            '/api',
            data=json.dumps(dict(
                jsonrpc='2.0',
                method='tutorial.hello',
                params=dict(title="TITLE"),
                id='1'))).data)
