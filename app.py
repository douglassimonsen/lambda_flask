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
    return 'b'


if __name__ == '__main__':
    app.run(debug=True)