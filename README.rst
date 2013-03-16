A Python dictionary implementation that supports properties::

    >>> from propdict import propdict
    >>> class Host(propdict):
    ...     ip_addr = None
    ...     use_zfs = True
    ...     @property
    ...     def netmask(self):
    ...         return '%s 255.255.255.0' % self.ip_addr


    >>> foo = Host(ip_addr='10.0.0.1')
    >>> foo
    propdict({'netmask': '10.0.0.1 255.255.255.0', 'ip_addr': '10.0.0.1', 'use_zfs': True})

This behaves just like a dictionary, for example you can pass it to any template::

    >>> rc_conf = '''hostname = %(ip_addr)s
    ... netmask = %(netmask)s'''
    >>> print rc_conf % foo
    hostname = 10.0.0.1
    netmask = 10.0.0.1 255.255.255.0


You can access values as properties or with the dict notation::

    >>> foo.ip_addr
    '10.0.0.1'
    >>> foo['ip_addr']
    '10.0.0.1'

And also properties::

    >>> foo['netmask']
    '10.0.0.1 255.255.255.0'
    >>> foo.netmask
    '10.0.0.1 255.255.255.0'

But you can also override properties by setting them::

    >>> foo.netmask = u'foo mask'
    >>> foo
    propdict({'netmask': u'foo mask', 'ip_addr': '10.0.0.1'})


Run Tests
=========

First::

    virtualenv .
    source bin/activate
    pip install pytest-cov

Then, to run tests::

    bin/py.test --cov propdict --cov-report html --cov-report term test_propdict.py

TODO
====

- [x] add documentation (examples: string templating)
- [x] eggify it
- [x] support class variables
- [ ] support iter(values|items|keys)
- [ ] travis
- [ ] check which python versions this actually works on (currently 2.7 tested)

