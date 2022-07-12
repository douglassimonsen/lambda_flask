from app import app
print(app({'rawPath': '/'}, ''))
import lambda_flask

print(lambda_flask.request.get_json())