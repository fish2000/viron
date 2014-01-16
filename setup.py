#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    VIRON -- Put environment variables in text file templates.
#
#    Copyright © 2012 Alexander Bohn
#
#    Permission is hereby granted, free of charge, to any person obtaining a copy 
#    of this software and associated documentation files (the "Software"), to deal 
#    in the Software without restriction, including without limitation the rights 
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
#    copies of the Software, and to permit persons to whom the Software is 
#    furnished to do so, subject to the following conditions:
#    
#    The above copyright notice and this permission notice shall be included in all 
#    copies or substantial portions of the Software.
#    
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
#    SOFTWARE.
#
from __future__ import print_function
import sys

name = 'viron'
version = '0.4.8'
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
    author=u"Alexander Bohn",
    author_email='fish2000@gmail.com',
    license='MIT',
    
    url='http://github.com/fish2000/%s/' % name,
    download_url='http://github.com/fish2000/%s/zipball/master' % name,
    install_requires=['argparse', 'argh'],
    
    package_dir={
        'viron': 'src/viron',
    },
    
    entry_points={
        'console_scripts': [
            'viron = viron.viron:main'
        ],
    },
    
    classifiers=classifiers+[
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7'],
)
