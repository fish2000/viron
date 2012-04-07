#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    VIRON -- Put environment variables in text file templates.
#
#    Copyright © 2012 Alexander Bohn
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#    
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import os, os.path
name = 'viron'
version = '0.1.8'
packages = []
description = 'Put environment variables in text file templates.'
keywords = 'python environment variable simple template text'

classifiers = [
    'Development Status :: 5 - Production/Stable']

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import shutil
if not os.path.exists('src/scripts'):
    os.makedirs('src/scripts')
if os.path.exists('src/scripts/viron'):
    os.remove('src/scripts/viron')
shutil.copyfile('src/viron/viron.py', 'src/scripts/viron')
os.chmod('src/scripts/viron', 0755)

setup(
    name=name, version=version, description=description,
    download_url = 'http://github.com/fish2000/%s/zipball/master' % name,

    author=u"Alexander Bohn",
    author_email='fish2000@gmail.com',
    url='http://github.com/fish2000/%s/' % name,
    license='GPLv2',
    
    keywords=keywords,
    platforms=['any'],
    packages=['viron'],
    package_dir={'viron': 'src/viron' },
    package_data={},
    scripts={
        'src/scripts/viron': 'viron' },
    
    install_requires=[
        'argparse',
        'argh'],
    
    classifiers=classifiers+[
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Operating System :: MacOS',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: OS Independent',
    'Operating System :: POSIX',
    'Operating System :: Unix',
    'Programming Language :: Python :: 2.6'],
)
