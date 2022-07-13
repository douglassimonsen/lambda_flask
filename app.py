__name__ = "hi"
if __name__ == '__main__':
    import flask
else:
    import lambda_flask as flask


app = flask.Flask(__name__)


@app.route('/')
def test1():
    return 'a'


@app.route('/help')
def test2():
    print(flask.request.get_json())
    return 'b'


if __name__ == '__main__':
    app.run(debug=True)

evt = {
        "version": "2.0",
        "routeKey": "ANY /{proxy+}",
        "rawPath": "/help",
        "rawQueryString": "",
        "headers": {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate",
            "content-length": "6",
            "content-type": "application/x-www-form-urlencoded",
            "host": "wmsqb2vrw7.execute-api.us-east-1.amazonaws.com",
            "user-agent": "python-requests/2.27.1",
            "x-amzn-trace-id": "Root=1-62cf2ad6-08dcd67862f1b6390676ade2",
            "x-forwarded-for": "98.46.0.170",
            "x-forwarded-port": "443",
            "x-forwarded-proto": "https"
        },
        "requestContext": {
            "accountId": "111263457661",
            "apiId": "wmsqb2vrw7",
            "domainName": "wmsqb2vrw7.execute-api.us-east-1.amazonaws.com",
            "domainPrefix": "wmsqb2vrw7",
            "http": {
                "method": "POST",
                "path": "/debug",
                "protocol": "HTTP/1.1",
                "sourceIp": "98.46.0.170",
                "userAgent": "python-requests/2.27.1"
            },
            "requestId": "VOOhlhv9oAMEMHQ=",
            "routeKey": "ANY /{proxy+}",
            "stage": "$default",
            "time": "13/Jul/2022:20:28:06 +0000",
            "timeEpoch": 1657744086756
        },
        "pathParameters": {
            "proxy": "debug"
        },
        "body": "aGk9Ynll",
        "isBase64Encoded": True
    }

print(app(evt, {}))