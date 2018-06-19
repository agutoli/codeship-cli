from setuptools import setup

setup(
    name='codeship_cli',
    version='0.0.5',
    packages=['codeship_cli', 'codeship_cli.commands'],
    scripts=['bin/codeship'],
    description = 'Codeship client to help find text, see configurations by terminal',
    license='Codeship cli to manipulate projects',
    author = 'Bruno Agutoli',
    author_email = 'bruno.agutoli@gmail.com',
    url = 'https://github.com/agutoli/codeship-cli',
    download_url = 'https://github.com/agutoli/codeship-cli/archive/master.zip',
    keywords = ['codeship', 'ci', 'codedeploy'],
    install_requires=[
        'requests==2.18.4',
        'pyyaml==3.12',
        'boto3==1.7.22'
    ],
    long_description=open('README.md').read(),
)
