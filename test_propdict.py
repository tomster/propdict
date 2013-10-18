from pytest import fixture, raises
from propdict import propdict

config = {
    'jailzfs': 'jails/ezjail',
    'ip_addr': '127.0.0.2',
}


class JailHost(propdict):

    jailzfs = None
    ip_addr = None
    use_zfs = True

    @property
    def netmask(self):
        return '%s 255.255.255.0' % self.ip_addr

    def notindict(self):
        return '%s is not in the dictionary representation' % self.ip_addr


@fixture
def host(request):
    return JailHost(**config)


@fixture
def netmask(host):
    return '%s 255.255.255.0' % host.ip_addr


def test_from_dict():
    pd = propdict({'a': 1})
    assert pd.items() == [('a', 1)]
    assert pd['a'] == 1
    assert pd.a == 1


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


def test_prop_keys(host):
    assert 'netmask' in host.keys()


def test_prop_iterkeys(host):
    assert 'netmask' in host.iterkeys()


def test_property_access(host, netmask):
    assert host.netmask == netmask


def test_property_in_items(host, netmask):
    assert ('netmask', netmask) in host.items()


def test_property_in_iteritems(host, netmask):
    assert ('netmask', netmask) in host.iteritems()


def test_property_as_dict(host):
    assert 'netmask' in host
    assert host['netmask'] == host.netmask


def test_class_variable_as_dict(host):
    assert 'use_zfs' in host.keys()
    assert 'use_zfs' in host
    assert host['use_zfs'] == host.use_zfs


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


def test__dict__(host):
    assert host.__dict__ == {'use_zfs': True, 'netmask': '127.0.0.2 255.255.255.0', 'ip_addr': '127.0.0.2', 'jailzfs': 'jails/ezjail'}


def test_set_builtin_method(host):
    with raises(TypeError):
        host.__getattribute__ = u'foo'


def test_get_property(host, netmask):
    assert host.get('netmask', None) == netmask


def test_get_property_default(host, netmask):
    assert host.get('netmask-extra', None) is None


def test_len(host):
    assert len(host) == 4  # jailzfs + ip_addr + use_zfs + netmask


def test_getattr(host, netmask):
    assert getattr(host, 'netmask') == netmask


def test_setattr(host, netmask):
    setattr(host, 'netmask', u'foo')
    assert host.netmask == u'foo'


def test_pop(host, netmask):
    host.netmask = u'foo'
    assert host.pop('netmask') == u'foo'
    assert host.netmask == netmask
    # you cannot pop a property
    with raises(KeyError):
        assert host.pop('netmask') == netmask


def test_del(host, netmask):
    host.netmask = u'foo'
    del host['netmask']
    assert host.netmask == netmask
    # you cannot delete a property
    with raises(KeyError):
        del host['netmask']


def test_post_init_addition(host):
    host['foo'] = 'bar'
    assert host.foo == 'bar'
    assert 'foo' in host


def test_update(host, netmask):
    host.update(netmask=u'foo')
    assert host.netmask == u'foo'


def test_values(host, netmask):
    assert netmask in host.values()


def test_itervalues(host, netmask):
    assert netmask in host.itervalues()


def test_has_key(host):
    assert 'netmask' in host


def test_repr(host):
    assert host.__repr__().startswith('''propdict({''')


def test_is_equal(host, netmask):
    assert host == JailHost(**{
        'netmask': netmask,
        'ip_addr': host.ip_addr,
        'jailzfs': host.jailzfs})


def test_not_equal_missing(host, netmask):
    assert host != JailHost(**{
        'netmask': netmask,
        'jailzfs': host.jailzfs})


def test_not_equal_extra(host, netmask):
    assert host != JailHost(**{
        'netmask': netmask,
        'ip_addr': host.ip_addr,
        'extra': 'extra',
        'jailzfs': host.jailzfs})


def test_not_equal_not_propdict(host, netmask):
    assert host != {
        'netmask': netmask,
        'ip_addr': host.ip_addr,
        'jailzfs': host.jailzfs}


def test_copy(host, netmask):
    copy = host.copy()
    assert copy == host
    copy['netmask'] = u'new'
    assert host['netmask'] != copy['netmask']
    assert copy != host
