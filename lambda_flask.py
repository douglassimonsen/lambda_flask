import flask_json as json


class Flask:
    def __init__(self, name) -> None:
        self.name = name
        self.routes = {}
        self.json_encoder = json.JSONEncoder()

    def route(self, raw_path):
        def route_wrapper(func=None):
            self.routes[raw_path] = func
            return func
        
        return route_wrapper
    
    def run(self, **kwargs):
        pass