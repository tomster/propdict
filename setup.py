from setuptools import setup
version = '1.1'

setup(
    version=version,
    name='propdict',
    description='A Python dictionary implementation that supports properties, class variables and inheritance for your sophisticated templating needs.',
    long_description=open('README.rst').read(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
    ],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    author='Tom Lazar',
    author_email='tom@tomster.org',
    url='https://github.com/tomster/propdict',
    license='BSD',
    zip_safe=False,
    install_requires=[],
    extras_require={
        "tests": [
            'pytest-cov',
            'pytest-flakes',
            'pytest-pep8'],
    },
    py_modules=['propdict'])
