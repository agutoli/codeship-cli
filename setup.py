from setuptools import setup

setup(
    name='codeship',
    version='0.0.1',
    packages=['codeship', 'codeship.commands'],
    scripts=['bin/codeship'],
    license='Codeship cli to manipulate projects',
    install_requires=[
        'requests==2.18.4',
        'pyyaml==3.12',
    ],
    long_description=open('README.md').read(),
)
