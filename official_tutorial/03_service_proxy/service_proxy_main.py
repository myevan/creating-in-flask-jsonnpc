if __name__ == '__main__':
    from flask_jsonrpc.proxy import ServiceProxy

    proxy = ServiceProxy('http://localhost:5000/api')
    print proxy.tutorial.hello('Jaru')
