class propdict(dict):

    def __init__(self, **config):
        for key, value in config.pop('host').items():
            self[key] = value

    def __getitem__(self, key):
        if key in self.keys():
            return dict.__getitem__(self, key)
        else:
            return getattr(self, key)

    def __getattribute__(self, name):
        try:
            return dict.__getitem__(self, name)
        except KeyError:
            return object.__getattribute__(self, name)
