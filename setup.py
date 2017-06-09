#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import os
from distutils.core import setup

from setuptools import find_packages


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()

version_tuple = __import__('django_js_choices').VERSION
version = '.'.join([str(v) for v in version_tuple])

setup(
    name='django-js-choices',
    version=version,
    description='Javascript model field choices handling for Django.',
    long_description=read('README.rst'),
    url='https://github.com/lorinkoz/django-js-choices',
    download_url='http://pypi.python.org/pypi/django-js-choices/',
    author='Lorenzo Peña',
    author_email='lorinkoz@gmail.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='django javascript model field choices',
    packages=find_packages(),
    package_data={
        'django_js_choices': [
            'templates/django_js_choices/*',
        ]
    },
    install_requires=[
        'Django>=1.5',
    ]
)
