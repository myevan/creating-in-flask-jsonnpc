from flask import Flask
from flask_jsonrpc import JSONRPC

app = Flask(__name__)

rpc = JSONRPC(app, '/api', enable_web_browsable_api=True)

@rpc.method('tutorial.hello(name=str)')
def hello(name):
    app.logger.debug('tutorial.hello:{0}'.format(name))

    return u'Hello, {0}!'.format2(name)


if __name__ == '__main__':
    import json
    import time

    app.debug = False
    with app.test_client() as client:
        print(client.post(
            '/api',
            data=json.dumps(dict(
                jsonrpc='2.0',
                method='tutorial.hello',
                params=dict(name='jaru'),
                id='1'))).data)

    time.sleep(0.5)
    app.debug = True
    with app.test_client() as client:
        print(client.post(
            '/api',
            data=json.dumps(dict(
                jsonrpc='2.0',
                method='tutorial.hello',
                params=dict(name='jaru'),
                id='1'))).data)
