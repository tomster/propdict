from pytest import fixture, raises
from propdict import propdict, dictproperty

config = {
    'jailzfs': 'jails/ezjail',
    'ip_addr':  '127.0.0.2',
}


class JailHost(propdict):

    jailzfs = None
    ip_addr = None
    use_zfs = True

    @dictproperty
    def netmask(self):
        return '%s 255.255.255.0' % self.ip_addr

    def notindict(self):
        return '%s is not in the dictionary representation' % self.ip_addr

    @property
    def regular_property(self):
        return '%s regular property' % self.ip_addr


@fixture
def host(request):
    return JailHost(**config)


@fixture
def netmask(host):
    return '%s 255.255.255.0' % host.ip_addr


def test_dict_from_class(host):
    assert host['ip_addr'] == config['ip_addr']


def test_property_from_class(host):
    assert host.use_zfs


def test_property_from_class_override():
    no_zfs = config.copy()
    no_zfs['use_zfs'] = False
    host = JailHost(**no_zfs)
    assert not host['use_zfs']
    assert not host.use_zfs


def test_property_from_instance(host):
    assert host.ip_addr == config['ip_addr']


def test_property_in_dict(host, netmask):
    assert host['netmask'] == host.netmask
    assert host.__dict__ == dict(config, netmask=netmask)


def test_prop_keys(host):
    assert 'netmask' in host.keys()


def test_property_access(host, netmask):
    assert host.netmask == netmask


def test_property_in_items(host, netmask):
    assert ('netmask', netmask) in host.items()


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


def test_regular_property(host):
    assert 'regular_property' not in host
    assert host.regular_property == '%s regular property' % host.ip_addr


def test_get_property(host, netmask):
    assert host.get('netmask', None) == netmask


def test_get_property_default(host, netmask):
    assert host.get('netmask-extra', None) is None


def test_len(host):
    assert len(host) == 3  # jailzfs + ip_addr + netmask


def test_getattr(host, netmask):
    assert getattr(host, 'netmask') == netmask


def test_setattr(host, netmask):
    setattr(host, 'netmask', u'foo')
    assert host.netmask == u'foo'
