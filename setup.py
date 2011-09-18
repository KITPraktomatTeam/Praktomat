#!/usr/bin/env python
import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='Praktomat',
    version='0.1',
    url='http://pp.info.uni-karlsruhe.de/project.php?id=34&lang=en',
    license = 'GPL',
    description='Quality control for programming assignments',
    long_description = read('README.md'),

    author='IPD Snelting, KIT',
    author_email='praktomat@googlemail.com',

    packages = find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data = True,

    install_requires = ['setuptools',
                        'ElementTree',
                        'Markdown >= 2.0.2',
                        #'MySQL-python >= 1.2.3c1',
                        'psycopg2 == 2.2.2', # PostgresSQL support
                        'Pygments >= 1.1.1',
                        'Werkzeug >= 0.5.1',
                        'django-extensions >= 0.4.1',
                        'South', # intelligent schema and data migrations
                        'django-tinymce', # widget to render a form field as a TinyMCE editor 
                        'chardet', # autodetect file encodings
						'M2Crypto', # Signing uploaded files
                        ],

    classifiers = [
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Education :: Testing',
    ]
)