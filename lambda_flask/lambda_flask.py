from . import flask_json as _json
CORS_HEADERS = {
    "Access-Control-Allow-Headers" : "Content-Type",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "*"
};

class Flask:
    def __init__(self, name) -> None:
        self.name = name
        self.routes = {}
        self.json_encoder = _json.JSONEncoder()

    def __call__(self, evt, context) -> dict:
        """
        This function is the entrypoint for the lambda function
        """
        resp = self.exec_route(evt['rawPath'])
        return self.CORS(resp)

    def route(self, raw_path):
        def route_wrapper(func=None):
            self.routes[raw_path] = func
            return func
        
        return route_wrapper
    
    def run(self, **kwargs):
        pass

    def CORS(self, msg):
        if 'headers' in msg:
            headers = {**CORS_HEADERS, **msg['headers']}
        else:
            headers = {**CORS_HEADERS}
        msg['headers'] = headers
        return msg

    def exec_route(self, raw_path):
        if raw_path not in self.routes:
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
        
        return {
            'statusCode': 200,
            'body': resp,
        }