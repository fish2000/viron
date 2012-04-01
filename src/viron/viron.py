#!/usr/bin/env python
# encoding: utf-8
"""
VIRON -- Put environment variables in text file templates.

The VIRON License Agreement (MIT License)
------------------------------------------

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

Copyright © 2012 Alexander Bohn.
This software is licensed under the terms of the GNU General Public
License version 2 as published by the Free Software Foundation.

"""
import sys, os, re
from string import Template
from argh import ArghParser, command, arg

@command
def text(swaptext, swapdic=os.environ, dumpstride=3):
    
    """ Simplistically replace any and all environment-variable-esque 
    $VAR_LABEL declarations in `swaptext` with content, as per the
    `swapdic` mapping, *qua* said declared labels. """
    
    matcher = r'(?<!\\)\${1}([A-Z][A-Z0-9_]+)'
    bracedmatcher = r'(?<!\\)\${1}\{([A-Z][A-Z0-9_]+)\}'
    swapmapper = lambda envname: envname and (envname, swapdic.get(envname, envname)) or ''
    
    envs = dict(map(swapmapper,
        re.compile(matcher).findall(swaptext)))
    envs.update(dict(map(swapmapper,
        re.compile(bracedmatcher).findall(swaptext))))
    
    strays = set(envs.keys()).difference(swapdic.keys())
    
    for stray in strays:
        print >>sys.stderr, "Warning: unmapped template label %s" % stray
    
    if len(strays) > 0:
        valids = sorted(swapdic.keys(), key=lambda v: len(v))
        strident = "%%-%ds" % len(list(reversed(valids))[0])
        print >>sys.stderr, "Valid template labels are:\n"
        for stride in [valids[i:dumpstride+i] for i in xrange(0, len(valids), dumpstride)]:
            print >>sys.stderr, ": ".join([strident % step for step in stride])
    
    return Template(
        re.sub(r'(\$+?)(?![A-Z0-9\{]+?)', '\g<0>\g<1>', swaptext,
            flags=re.MULTILINE)).safe_substitute(**envs)

@arg('pth', help="File path from which to load text for viron agumentation")
def filepath(args):
    try:
        with open(args.pth, 'r') as filepth:
            return text(filepth.read())
    except IOError, err:
        print >>sys.stderr, "File path %s is totally invalid." % pth
        print >>sys.stderr, unicode(err).encode('UTF-8')
        sys.exit(1)

p = ArghParser()
p.add_commands([text, filepath])

if __name__ == "__main__":
    yodogg = """

    DEBUG = True

    TM_SELECTED_FILE = $TM_SELECTED_FILE
    COMMAND_MODE = $COMMAND_MODE
    TM_PROJECT_FILEPATH = $TM_PROJECT_FILEPATH
    DJANGO_SETTINGS_MODULE = $DJANGO_SETTINGS_MODULE

    $

    import os
    virtualpath = lambda *pths: os.path.join('$VIRTUAL_ENV', *pths)

    HOME = \$HOME
    
    SECURITYSESSIONID = ${SECURITYSESSIONID}
    PYTHONPATH = ${PYTHONPATH}DOGG
    
    $ $ $
    $$ $$$ $$$$
    
    ${
    
    
    DATABASES = {
        "default": {
            # Ends with "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
            "ENGINE": "django.db.backends.sqlite3",
            # DB name or path to database file if using sqlite3.
            "NAME": "dev-$INSTANCE_NAME.db",
            # Not used with sqlite3.
            "USER": "",
            # Not used with sqlite3.
            "PASSWORD": "",
            # Set to empty string for localhost. Not used with sqlite3.
            "HOST": "",
            # Set to empty string for default. Not used with sqlite3.
            "PORT": "",
        }
    }

    """
    p.dispatch()
