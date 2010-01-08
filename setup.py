#!/usr/bin/env python

from distutils.core import setup

README_FILE = open('README.txt')
try:
    long_description = README_FILE.read()
finally:
    README_FILE.close()

setup(name='nano',
        version='0.2',
        packages=('nano',),
        platforms=['any'],
        description='Does less! Loosely coupled mini-apps for django.',
        author_email='kaleissin@gmail.com',
        author='kaleissin',
        long_description=long_description,
        url='http://code.google.com/p/django-nano/',
        download_url='http://code.google.com/p/django-nano/source/checkout',
        classifiers=[
                'Development Status :: 4 - Beta',
                'Environment :: Web Environment',
                'Framework :: Django',
                'Intended Audience :: Developers',
                'License :: OSI Approved :: MIT License',
                'Operating System :: OS Independent',
                'Programming Language :: Python',
                'Topic :: Software Development :: Libraries :: Application Frameworks',
                'Topic :: Software Development :: Libraries :: Python Modules',
        ]
)
