#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
VIRON -- Put environment variables in text file templates.

Copyright 2012 Alexander Bohn.

The VIRON License Agreement (MIT License)
------------------------------------------

Permission is hereby granted, free of charge, to any person obtaining a copy 
of this software and associated documentation files (the "Software"), to deal 
in the Software without restriction, including without limitation the rights 
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
copies of the Software, and to permit persons to whom the Software is 
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
SOFTWARE.

"""

import sys
import os
import re
from string import Template
from argh import ArghParser, command, arg


@command
def viron(swaptext, swapdic=os.environ, ignoreseq=tuple(),
    dumpstride=3, warn_unmapped_labels=True):

    """ Simplistically replace any and all environment-variable-esque
    $VAR_LABEL declarations in :`swaptext` with content, as per the
    :`swapdic` mapping, *qua* said declared labels. """

    matcher = r'(?<!\\)\${1}([A-Z][A-Z0-9_]+)'
    bracedmatcher = r'(?<!\\)\${1}\{([A-Z][A-Z0-9_]+)\}'
    swapmapper = lambda en: en and (en, swapdic.get(en, "$%s" % en)) or ''
    swapfilter = lambda ex: ex and not (ex in ignoreseq)
    
    envs = dict(map(swapmapper, filter(swapfilter,
        re.compile(matcher).findall(swaptext))))
    envs.update(dict(map(swapmapper, filter(swapfilter,
        re.compile(bracedmatcher).findall(swaptext)))))

    strays = set(envs.keys()).difference(swapdic.keys())

    if warn_unmapped_labels and len(strays) > 0:
        for stray in strays:
            print >>sys.stderr, "Warning: unmapped template label %s" % stray
        valids = sorted(filter(
            lambda s: s.isupper() and not s.startswith('_'),
                swapdic.keys()), key=len)
        strident = "%%-%ds" % len(list(reversed(valids))[0])
        stride = xrange(0, len(valids), dumpstride)
        print >>sys.stderr, "Valid template labels:\n"
        for stride in [valids[i:dumpstride+i] for i in stride]:
            print >>sys.stderr, ": ".join([strident % step for step in stride])

    return Template(
        re.sub(r'(\$+?)(?![A-Z0-9\{]+?)', '\g<0>\g<1>', swaptext,
            flags=re.MULTILINE)).safe_substitute(**envs)


def filepath(pth, ignoreseq=tuple(),
    dumpstride=3, warn_unmapped_labels=True):
    try:
        with open(pth, 'r') as filepth:
            return viron(filepth.read(),
                ignoreseq=ignoreseq,
                dumpstride=dumpstride,
                warn_unmapped_labels=warn_unmapped_labels)
    except IOError, err:
        print >>sys.stderr, "File path %s is totally invalid." % pth
        print >>sys.stderr, unicode(err).encode('UTF-8')
        sys.exit(1)


def stdinput(ignoreseq=tuple(), dumpstride=3):
    while 1:
        try:
            line = sys.stdin.readline()
        except KeyboardInterrupt:
            break

        if not line:
            break

        sys.stdout.write(viron(line,
            ignoreseq=ignoreseq,
            dumpstride=dumpstride,
            warn_unmapped_labels=False))
    return ''

@arg('TEXT', nargs='?', default=None,
    help="Text to process")
@arg('-f', '--file', nargs='?', default=None,
    help="File path from which to load text for viron agumentation")
@arg('-S', '--dump-stride', default=3,
    help="Number of columns to print when listing valid template labels")
@arg('-i', '--ignore', default="",
    help="Comma-separated list of labels to ignore")
@arg('-q', '--quiet', action='store_true',
    help="Don't issue warnings on STDERR about unknown template labels")
def text(args):
    warn_unmapped_labels = (not args.quiet)
    ignoreseq = tuple(str(args.ignore).upper().split(','))
    if args.dump_stride < 1:
        warn_unmapped_labels = False
    if args.TEXT is None:
        if args.file is None:
            return stdinput(ignoreseq=ignoreseq,
                dumpstride=args.dump_stride)
        else:
            return filepath(args.file,
                ignoreseq=ignoreseq,
                dumpstride=args.dump_stride,
                warn_unmapped_labels=warn_unmapped_labels)
    else:
        if args.file is not None:
            print >>sys.stderr, "Warning: reading from %s (ignoring text '%s')" % (args.file, args.TEXT)
            return filepath(args.file, ignoreseq=ignoreseq,
                dumpstride=args.dump_stride)
        else:
            return viron(args.TEXT, ignoreseq=ignoreseq,
                dumpstride=args.dump_stride,
                warn_unmapped_labels=warn_unmapped_labels)


p = ArghParser()
p.add_commands([text, filepath])

def main():
    argv = list(sys.argv[1:])
    cmdarg = argv[0:1]
    if len(cmdarg) > 0:
        cmd = cmdarg[0]
    else:
        cmd = None
    if cmd is not None and cmd not in ('text', 'filepath'):
        argv.insert(0, 'text')
    p.dispatch(argv=argv)

if __name__ == "__main__":
    main()

