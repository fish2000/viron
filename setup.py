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
from __future__ import print_function
import sys

name = 'viron'
version = '0.3.3'
packages = []
description = 'Put environment variables in text file templates.'
keywords = 'python environment variable simple template text'

classifiers = [
    'Development Status :: 5 - Production/Stable']

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if 'sdist' in sys.argv and 'upload' in sys.argv:
    import commands
    import os
    finder = "/usr/bin/find %s \( -name \*.pyc -or -name .DS_Store \) -delete"
    theplace = os.getcwd()
    if theplace not in (".", "/"):
        print("+ Deleting crapola from %s..." % theplace)
        print("$ %s" % finder % theplace)
        commands.getstatusoutput(finder % theplace)
        print("")

setup(
    name=name, version=version, description=description,
    keywords=keywords, platforms=['any'], packages=['viron'],
    
    author=u"Alexander Bohn", author_email='fish2000@gmail.com',
    
    license='GPLv2',
    url='http://github.com/fish2000/%s/' % name,
    download_url='http://github.com/fish2000/%s/zipball/master' % name,
    
    entry_points={
        'console_scripts': ['viron = viron.viron:main'] },
    
    package_dir={
        'viron': 'src/viron' },
    
    install_requires=[
        'argparse', 'argh'],
    
    classifiers=classifiers+[
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.6'],
)
