

def dictproperty(method):
    method.in_dict = True
    return method


class propdict(dict):

    def __new__(cls, **kw):
        cls.dict_properties = set()
        for name, method in cls.__dict__.iteritems():
            if hasattr(method, "in_dict"):
                cls.dict_properties.add(name)
        return dict.__new__(cls, **kw)

    def __init__(self, **config):
        for key, value in config.pop('host').items():
            self[key] = value
        for name, method in self.__dict__.iteritems():
            if hasattr(method, "in_dict"):
                self.dict_properties.add(name)

    def __getitem__(self, key):
        if key in dict.keys(self):
            return dict.__getitem__(self, key)
        else:
            return getattr(self, key)

    def keys(self):
        dict_keys = dict.keys(self)
        return list(set(dict_keys).union(self.dict_properties))

    @property
    def __dict__(self):
        result = self
        for propkey in self.dict_properties:
            if propkey not in self:  # dict values take precedence
                result[propkey] = self[propkey]()
        return result

    def __setattr__(self, name, value):
        if name in dir(self) and not name in self.keys():
            raise TypeError("cannot overwrite existing method")
        self[name] = value

    def __getattribute__(self, name):
        try:
            return dict.__getitem__(self, name)
        except KeyError:
            return object.__getattribute__(self, name)
