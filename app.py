# import flask
import lambda_flask as flask


app = flask.Flask(__name__)


@app.route('/')
def test1():
    return 'a'


@app.route('/help')
def test2():
    return 'b'


app.run(debug=True)
# app.routes['/help']()
