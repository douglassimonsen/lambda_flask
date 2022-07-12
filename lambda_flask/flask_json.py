import json

class JSONEncoder:
    def __init__(self) -> None:
        pass

    def default(obj) -> str:
        return json.dumps(obj)