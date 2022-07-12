def route_wrapper_factory():
    def route_wrapper(func):
        return func()
    
    return route_wrapper


class Flask:
    def __init__(self, name) -> None:
        self.name = name
        self.routes = {}

    def route(self, raw_path):
        tmp = route_wrapper_factory()
        self.routes[raw_path] = tmp
        return tmp
    
    def run(self, **kwargs):
        pass