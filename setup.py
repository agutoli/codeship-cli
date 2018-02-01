from setuptools import setup
from setuptools.command.install import install
import setuptools.command.build_py
import os


# class new_install(install):
#     def __init__(self, *args, **kwargs):
#         super(new_install, self).__init__(*args, **kwargs)
#         # atexit.register(_post_install)

class PostInstallCommand(setuptools.command.build_py.build_py):
    def run(self):
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
        os.system("python setup.py build")

setup(
    name='codeship',
    version='0.0.1',
    packages=['codeship', 'codeship.commands'],
    scripts=['bin/codeship'],
    license='Codeship cli to manipulate projects',
    # cmdclass={'build_py': PostInstallCommand},
    install_requires=[
        'requests==2.18.4',
        'pyyaml==3.12',
    ],
    long_description=open('README.md').read(),
)
