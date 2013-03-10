from pytest import fixture
from foo import JailHost

config = {
    'host': {
        'jailzfs': 'jails/ezjail',
        'ip_addr':  '127.0.0.2',
    },
    'cleanser': {
        'user': 'cleanser',
    }
}


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
    assert 'netmask' in host.keys()


def test_property_access(host):
    assert host.netmask == '%s 255.255.255.0' % host.ip_addr
