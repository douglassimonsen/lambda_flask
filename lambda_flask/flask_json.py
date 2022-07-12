import json

class JSONEncoder:
    def __init__(self) -> None:
        pass

    def default(self, obj) -> str:
        return json.dumps(obj)