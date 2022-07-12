


class Flask:
    def __init__(self, name) -> None:
        self.name = name
        self.routes = {}

    def route(self, raw_path):
        def route_wrapper(func=None):
            self.routes[raw_path] = func
            return func
        
        return route_wrapper
    
    def run(self, **kwargs):
        pass