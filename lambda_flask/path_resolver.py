paths = {
    '/': lambda: 1,
    '/<name>/thing': lambda name: f"hi, {name}",
    '/<int:id>/x': lambda id: id * 2,
    '/<string:name>/<int:x>/asd': lambda name, number: f"{number} / {name}",
}


def gen_layer_func(typ):
    def inner(m):
        try:
            return typ(m)
        except:
            return None
    
    return inner


class PathResolver:
    def __init__(self, paths) -> None:
        self.paths = paths
        self.simple_paths = {}
        self.complex_paths = {}
        self.layer_types = {  # we're not including path because that would require regex
            'int': gen_layer_func(int),
            'float': gen_layer_func(float),
            'string': gen_layer_func(str),
        }
        self.gen_resolvers()

    def gen_resolvers(self):
        def gen_resolver(layer_funcs):
            def resolver(new_path):
                new_layers = new_path[1:].split('/')
                if len(new_layers) != len(layer_funcs):
                    return False, []
                candidate = [lf(nl) for lf, nl in zip(layer_funcs, new_layers)]
                return all(x is not None for x in candidate), [x for x in candidate if x is not ...]
            
            return resolver
        
        def wrapper(l):
            def inner(m):
                return ... if m == l else None  # "..." is pretty smelly, but it's a nice way to denote a neutral, non-null value
        
            return inner
        
        for path, path_func in self.paths.items():
            if '<' not in path:
                self.simple_paths[path] = path_func
            else:
                layers = path[1:].split('/')
                layer_funcs = []
                for l in layers:
                    if not l.startswith("<"):
                        layer_funcs.append(wrapper(l))
                    elif ':' in l:
                        layer_funcs.append(self.layer_types[l[1:].split(':', 1)[0]])
                    else:
                        layer_funcs.append(lambda m: m)
                self.complex_paths[gen_resolver(layer_funcs)] = path_func

    def resolve(self, new_path):
        if new_path in self.simple_paths:
            return self.simple_paths[new_path]()
        for path_resolver, path_func in self.complex_paths.items():
            is_valid, vars = path_resolver(new_path)
            if is_valid:
                return path_func(*vars)


pr = PathResolver(paths)
print(pr.resolve('/'))
print(pr.resolve('/matt/thing'))
print(pr.resolve('/1/x'))
print(pr.resolve('/matt/1/asd'))