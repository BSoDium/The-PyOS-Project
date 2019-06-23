class Response:

    def __init__(self, properties, status_code=None):
        valid_props = (list, tuple)
        if not isinstance(properties, valid_props):
            raise ValueError("Argument 'properties' should be type 'list' or 'tuple', not '{}'".format(type(properties)))

        self.status_code = status_code if status_code is not None else None
        self.properties = list(properties)

    def __repr__(self):
        def rend(d, l, root=None):
            root = root or []

            for key, val in d.items():
                if isinstance(val, dict):
                    rend(val, l, root+[key])
                else:
                    l.append("{par}{key} = {val}".format(par=''.join([parent+'.' for parent in root]), key=key, val=repr(val)))

        l = []
        rend(self._dict, l)
        return "[pypresence.Response\n    {}\n]".format('\n    '.join(l))

    def __str__(self):
        return self.__repr__()

    def to_dict(self):
        fdict = {}
        for p in self.properties:
            prop = getattr(self, p)
            if isinstance(prop, Response):
                fdict[p] = prop.to_dict()
            else:
                fdict[p] = getattr(self, p)
        return fdict

    @classmethod
    def from_dict(cls, from_dict: dict, status_code=None):

        if not isinstance(from_dict, dict):
            raise ValueError("Expected type 'dict' got type '{}' ".format(type(from_dict)))

        for key, value in from_dict.items():
            if isinstance(value, dict):
                value = Response.from_dict(value)
            setattr(cls, key, value)

        cls._dict = from_dict

        return cls(list(from_dict.keys()), status_code)

    def __getattr__(self, attr: str):  # Add shorthand for the payload's data
        data = getattr(self, 'data', None)
        if data and attr in self.data:
            return self.data.attr
        return self.attr

    def set_prop(self, name, value):
        for n in self.properties:
            if n == name:
                setattr(self,name,value)
                break
            elif isinstance(getattr(self, n), Response):
                getattr(self, n).set_prop(name,value)


    def get_prop(self, name):
        for n in self.properties:
            if n == name:
                return getattr(self,name)
                break
            elif isinstance(getattr(self, n), Response):
                r = getattr(self, n).get_prop(name)
                if r != None:
                    return r
