from pytest import fixture, raises
from propdict import propdict, dictproperty

config = {
    'host': {
        'jailzfs': 'jails/ezjail',
        'ip_addr':  '127.0.0.2',
    },
    'cleanser': {
        'user': 'cleanser',
    }
}


class JailHost(propdict):

    jailzfs = None
    ip_addr = None

    blueprints = None
    jails = None
    use_zfs = True

    @dictproperty
    def netmask(self):
        return '%s 255.255.255.0' % self.ip_addr

    def notindict(self):
        return '%s is not in the dictionary representation' % self.ip_addr


@fixture
def host(request):
    return JailHost(**config)


def test_dict_from_class(host):
    assert host['ip_addr'] == config['host']['ip_addr']


def test_property_from_class(host):
    assert host.use_zfs


def test_property_from_class_override():
    no_zfs = config.copy()
    no_zfs['host']['use_zfs'] = False
    host = JailHost(**no_zfs)
    assert not host['use_zfs']
    assert not host.use_zfs


def test_property_from_instance(host):
    assert host.ip_addr == config['host']['ip_addr']


def test_property_in_dict(host):
    assert host['netmask'] == host.netmask


def test_prop_keys(host):
    assert 'netmask' in host.keys()


def test_property_access(host):
    assert host.netmask == '%s 255.255.255.0' % host.ip_addr


def test_as_dict(host):
    assert 'netmask' in host
    assert host['netmask'] == host.netmask


def test_methods_not_in_dict(host):
    assert 'notindict' not in host


def test_method_access(host):
    assert host.notindict() == '%s is not in the dictionary representation' % host.ip_addr


def test_set_attribute(host):
    host.ip_addr = u'foo'
    assert host.ip_addr == u'foo'
    assert host['ip_addr'] == u'foo'


def test_set_property(host):
    host.netmask = u'foo'
    assert host.netmask == u'foo'
    assert host['netmask'] == u'foo'


def test_set_method(host):
    with raises(TypeError):
        host.notindict = u'foo'


def test_set_builtin_method(host):
    with raises(TypeError):
        host.__getattribute__ = u'foo'
