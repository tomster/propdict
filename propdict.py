class Foo(object):

    def __init__(self, foo=None):
        self.foo = foo

    def port(self, offset=0):
        return self.foo * 2 + offset


def annotate(obj, attr='__meta__', value=None):
    obj.__setattr__(attr, value)


class JailHost(dict):

    jailzfs = None
    ip_addr = None

    blueprints = None
    jails = None
    use_zfs = True

    def __init__(self, **config):
        for key, value in config.pop('host').items():
            self[key] = value
            print "setting %s to %s" % (key, value)

    @property
    def netmask(self):
        return '%s 255.255.255.0' % self.ip_addr

    def __getitem__(self, key):
        if key in self.keys():
            return dict.__getitem__(self, key)
        else:
            return getattr(self, key)

    def __getattribute__(self, name):
        # Default behaviour
        return object.__getattribute__(self, name)
