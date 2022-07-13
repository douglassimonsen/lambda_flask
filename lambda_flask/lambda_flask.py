from . import flask_json, utils
import json
import base64
import urllib.parse
import inspect
import pathlib
CORS_HEADERS = {
    "Access-Control-Allow-Headers" : "Content-Type",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "*"
};


def jsonify(obj):
    return obj


class request:
    @staticmethod
    def get_json():
        return {}


class Flask:
    def __init__(self, name) -> None:
        self.name = name
        self.routes = {}
        self.json_encoder = flask_json.JSONEncoder()
        self.evt = None
        self.context = None
        self.root_folder = pathlib.Path(inspect.stack()[1].filename).parent
        utils.request.get_json = self.tmp_get_json  # necessary to get flask functionality. Most likely to cause threading weirdness

    def __call__(self, evt, context) -> dict:
        """
        This function is the entrypoint for the lambda function
        """
        if evt.get('isBase64Encoded', False):
            evt['body'] = base64.b64decode(evt['body']).decode("utf-8")
        self.evt = evt
        self.context = context

        resp = self.exec_route()
        return self.CORS(resp)

    def route(self, raw_path):
        def route_wrapper(func=None):
            self.routes[raw_path] = func
            return func
        
        return route_wrapper
    
    def run(self, **kwargs):
        pass

    def CORS(self, msg):
        if "statusCode" not in msg:
            msg['statusCode'] = 200
        if "body" not in msg:
            msg['body'] = ""
        if 'headers' in msg:
            headers = {**CORS_HEADERS, **msg['headers']}
        else:
            headers = {**CORS_HEADERS}
        msg['headers'] = headers
        return msg

    def tmp_get_json(self):
        method = self.evt['requestContext']['http']['method']
        if method == 'GET':
            return self.evt.get('queryStringParameters', {})
        else:
            try:
                return json.loads(self.evt['body'])
            except json.decoder.JSONDecodeError:
                body = urllib.parse.parse_qs(self.evt['body'])
                return {k: v[0] for k, v in body.items()}
        return method

    @staticmethod
    def _get_content_type(suffix):
        content_map = {
            '.css': 'text/css',
            '.csv': 'text/csv',
            '.doc': 'application/msword',
            '.html': 'text/html',
            '.js': 'text/javascript',
            '.json': 'application/json',
            '.pdf': 'application/pdf',
            '.xml': 'application/xml',
            '.zip': 'application/zip',
        }
        return content_map.get(suffix, 'text/plain')

    def exec_route(self):
        raw_path = self.evt['rawPath']
        if raw_path == '/debug':  # special method to help with debugging, almost certainly a security vulnerability
            return {
                'statusCode': 200,
                'body': self.json_encoder.default({
                    'evt': self.evt,
                    'context': self.context,
                })
            }

        if raw_path not in self.routes:
            static_candidate = pathlib.Path(self.root_folder, 'static', raw_path[1:])
            if static_candidate.exists():  # if you tell me this is a race condition, I'll fight you

                return {
                    "body": open(static_candidate, 'rb').read(),
                    "headers": {"Content-Type": self._get_content_type(static_candidate.suffix)}
                }

            return {
                "statusCode": 404,
                "body": f"The path '{raw_path}' could not be found"
            }
        try:
            resp = self.routes[raw_path]()
        except Exception as e:
            return {
                "statusCode": 500,
                "body": f"The path '{raw_path}' experienced the following error:\n\n{repr(e)}"
            }
        
        try:
            resp = self.json_encoder.default(resp)
        except Exception as e:
            return {
                "statusCode": 500,
                "body": f"The path '{raw_path}' couldn't serialize the response ({repr(e)}):\n\n{str(resp)}"
            }
        
        if isinstance(resp, dict):
            return resp
        else:
            return {
                'body': str(resp),
            }