from setuptools import setup

setup(
    name='propdict',
    zip_safe=False,
    install_requires=[],
    extras_require={
        "tests": ['pytest-cov'],
    },
    packages=['.'])
