import sys

if sys.version_info[0] >= 3:  # pragma: no cover
    DICT_KEYS = [str, bool, int, float, dict, list, tuple, property]
else:  # pragma: no cover
    DICT_KEYS = [str, bool, int, float, __builtins__['unicode'], dict, list, tuple, property]


class propdict(dict):

    def __new__(cls, *args, **kw):
        cls.__dict_keys__ = set([
            name for name in dir(cls)
            if not name.startswith('_') and (type(getattr(cls, name)) in DICT_KEYS or getattr(cls, name) is None)])
        return dict.__new__(cls, *args, **kw)

    def keys(self):
        return list(set(dict.keys(self)).union(self.__dict_keys__))

    def __getitem__(self, key):
        if key in dict.keys(self):
            return dict.__getitem__(self, key)
        else:
            return getattr(self, key)

    def __getattribute__(self, name):
        try:
            return dict.__getitem__(self, name)
        except KeyError:
            return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        if name in dir(self) and not name in self.keys():
            raise TypeError("cannot overwrite existing method")
        self[name] = value

    def __repr__(self):
        r = ["{0!r}: {1!r}".format(k, v) for k, v in self.items()]
        return "propdict({" + ", ".join(r) + "})"

    @property
    def __dict__(self):
        return dict(self.items())

    def __contains__(self, name):
        return name in self.keys()

    has_key = __contains__

    def iterkeys(self):
        for key in self.keys():
            yield key

    def items(self):
        return [(key, self[key]) for key in self.keys()]

    def iteritems(self):
        for key in self.iterkeys():
            yield (key, self[key])

    def values(self):
        return [self[key] for key in self.keys()]

    def itervalues(self):
        for key in self.iterkeys():
            yield self[key]

    def __len__(self):
        return len(self.keys())

    def get(self, key, default=None):
        try:
            return self[key]
        except AttributeError:
            return default

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if set(self.keys()) != set(other.keys()):
            return False
        for key, value in self.items():
            if other[key] != value:
                return False
        return True

    def copy(self):
        copy = self.__class__()
        for key in dict.keys(self):
            copy[key] = self[key]
        return copy
