import json

class JSONEncoder:
    def __init__(self) -> None:
        pass

    def default(self, obj) -> str:
        if isinstance(obj, (list, dict)):
            return json.dumps(obj, indent=4, default=str)
        return str(obj)