# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.
from __future__ import print_function

try:
    import setuptools
except:
    print('''
setuptools not found.

On linux, the package is often called python-setuptools''')
    from sys import exit
    exit(1)
import os

exec(compile(open('rbit/rbit_version.py').read(), 'rbit/rbit_version.py', 'exec'))
long_description = open('README.rst').read()

undef_macros=[]
if os.environ.get('DEBUG'):
    undef_macros=['NDEBUG']

extensions = {
}

ext_modules = []

packages = setuptools.find_packages()

classifiers = [
]

setuptools.setup(name='rbit',
      version=__version__,
      description='Rbit: A New Type of Mail Client',
      long_description=long_description,
      author='Luis Pedro Coelho',
      author_email='luis@luispedro.org',
      license='Proprietary',
      platforms=['Any'],
      classifiers=classifiers,
      url='http://luispedro.org/software/rbit',
      packages=packages,
      ext_modules=ext_modules,
      test_suite='nose.collector',
      )

