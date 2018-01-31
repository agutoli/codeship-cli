from distutils.core import setup

setup(
    name='codeship',
    version='0.0.1',
    packages=['codeship', 'codeship.commands'],
    scripts=['bin/codeship'],
    license='Codeship cli to manipulate projects',
    long_description=open('README.md').read(),
)
