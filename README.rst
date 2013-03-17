A Python dictionary implementation that supports properties, class variables and inheritance for your sophisticated templating needs.

.. image:: https://travis-ci.org/tomster/propdict.png

Motivation
==========

Overriding a specific behavior of a class is easy: create a subclass (or even just an instance) and just implement the aspect you are interested with and be done. Not so with templates, though. If you want to change one part of it, you need to override the entire template, essentially forking the work of the template author.

``propdict`` counters this by allowing the template author to *put logic and behavior into the data* that goes into the template rather than the template itself.

A consumer of the template can then simply subclass the `propdict` based data, override the specific aspects and leave the template as-is.


Example
======= 

Say you're the author of a `set of templates for configuring *NIX style systems <https://github.com/ZeitOnline/briefkasten>`_. Naturally, a lot of these templates will be using the same values, for example the IP address of the machine being configured. Now, some *other* values in turn depend on the value of the IP address, too. Let's say one such file has a line configuring the network interface using a netmask, so you end up with a template containing the following snippet:

    >>> template = '''ifconfig_%(iface)s="inet %(ip_addr)s netmask %(netmask)s"'''

Given a dictionary with the necessary data, this would then evaluate to the following:

    >>> print template % dict(ip_addr='192.168.1.1', iface='em0', netmask='255.255.255.0')
    ifconfig_em0="inet 192.168.1.1 netmask 255.255.255.0"

This works fine for most cases, but what if a particular host you deploy is behind a NAT and needs an entirely different configuration that doesn't follow the above format? You now either need to create a custom version of the template (which, unlike the basic example above, could well be of non-trivial length and complexity) that differs in just that one line or the author of the template needs to work in (yet another) special edgecase that won't affect 99% of the users.

The third solution is to keep (that line of) the templates as simple as possible:

    >>> template = "%(ifconfig)s"

and put the logic into the dictionary. Like so:

    >>> from propdict import propdict
    >>> class Host(propdict):
    ...     ip_addr = None
    ...     iface = 'em0'
    ...     netmask = '255.255.255.0'
    ...     @property
    ...     def ifconfig(self):
    ...         return '''ifconfig_%(iface)s="inet %(ip_addr)s netmask %(netmask)s"''' % self


    >>> server_foo = Host(ip_addr='10.0.0.1')
    >>> print template % server_foo
    ifconfig_em0="inet 10.0.0.1 netmask 255.255.255.0"

So far so good, we got the same result as above. But let's consider another server:

    >>> server_bar = Host(ip_addr='10.0.0.2', ifconfig='ifconfig_em1="inet 10.0.0.2 netmask 255.255.0.0"')
    >>> print template % server_bar
    ifconfig_em1="inet 10.0.0.2 netmask 255.255.0.0"

Notice, how the new definition of ``ifconfig`` contains a new value for the interface (perhaps this host has two built-in) but still references ``ip_addr``. In this case it might be better to not simply provide a new, static value but to come up with a better implementation of the property:

    >>> class HostBar(Host):
    ...     iface_2 = 'em1'
    ...     @property
    ...     def ifconfig(self):
    ...         return '''ifconfig_%(iface_2)s="inet %(ip_addr)s netmask %(netmask)s"''' % self
    >>> server_bar = HostBar(ip_addr='10.0.0.2', netmask='255.255.0.0')
    >>> print template % server_bar
    ifconfig_em1="inet 10.0.0.2 netmask 255.255.0.0"

So, we were able to provide an arbitrary new value for the ``ifconfig`` key by changing just that and without touching the template, while still keeping the default behavior (it's automatically computed for you from the interface and IP address).


Basic Features
==============

``propdict`` instances behave almost exactly as a regular dictionary, except that you can access values using the dict notation or attribute notation:

    >>> server_foo.ip_addr
    '10.0.0.1'
    >>> server_foo['ip_addr']
    '10.0.0.1'

    >>> print server_foo['ifconfig']
    ifconfig_em0="inet 10.0.0.1 netmask 255.255.255.0"

    >>> print server_foo.ifconfig
    ifconfig_em0="inet 10.0.0.1 netmask 255.255.255.0"

The same works also for assignment:

    >>> server_foo.ip_addr = '192.168.1.1'
    >>> print server_foo.ip_addr
    192.168.1.1

    >>> server_foo['ip_addr'] = '127.0.0.1'
    >>> print server_foo.ip_addr
    127.0.0.1

Assignment also works for changing properties, of course, as you saw in the example:

    >>> server_foo.ifconfig = u'foo mask'
    >>> print server_foo.ifconfig
    foo mask

It is noteworthy, though, that you cannot delete properties. However, you *can* delete custom *values* of properties, but that just re-exposes their original value:

    >>> del server_foo['ifconfig']
    >>> print server_foo.ifconfig
    ifconfig_em0="inet 127.0.0.1 netmask 255.255.255.0"

    >>> del server_foo['ifconfig']
    Traceback (most recent call last):
    ...
    KeyError: 'ifconfig'


Run Tests
=========

To make sure that ``propdict`` works for your setup, run its tests. You need `py.test <http://pytest.org/latest/>`_, perhaps like so::

    virtualenv .
    source bin/activate
    pip install pytest-cov

Then, to run all tests (including this README)::

    bin/py.test

If you made some changes and want to know whether you broke coverage::

    bin/py.test --cov propdict --cov-report html --cov-report term test_propdict.py

TODO
====

- [x] add documentation (examples: string templating)
- [x] eggify it
- [x] support class variables
- [x] support iter(values|items|keys)
- [ ] travis
- [ ] check which python versions this actually works on (currently 2.7 tested)

