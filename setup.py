from setuptools import setup

setup(
    name='codeship_cli',
    version='0.0.3',
    packages=['codeship_cli', 'codeship_cli.commands'],
    scripts=['bin/codeship'],
    license='Codeship cli to manipulate projects',
    install_requires=[
        'requests==2.18.4',
        'pyyaml==3.12',
        'boto3==1.7.22'
    ],
    long_description=open('README.md').read(),
)
