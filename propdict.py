def dictproperty(method):
    method.__dictproperty__ = True
    return method


class propdict(dict):

    def __new__(cls, **kw):
        cls.__dict_properties__ = set()
        for name, method in cls.__dict__.iteritems():
            if hasattr(method, "__dictproperty__"):
                cls.__dict_properties__.add(name)
        return dict.__new__(cls, **kw)

    def __contains__(self, name):
        return name in self.keys()

    def __getitem__(self, key):
        if key in dict.keys(self):
            return dict.__getitem__(self, key)
        else:
            return getattr(self, key)

    def keys(self):
        return list(set(dict.keys(self)).union(self.__dict_properties__))

    @property
    def __dict__(self):
        result = self
        for propkey in self.__dict_properties__:
            if propkey not in dict.keys(self):  # dict values take precedence
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
            item = object.__getattribute__(self, name)
            if hasattr(item, "__dictproperty__"):
                return item()
            else:
                return item
