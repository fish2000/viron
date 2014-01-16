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
from __future__ import print_function

import sys
import os
import re
from string import Template
from argh import ArghParser, command, arg

@command
def viron(swaptext, swapdic=os.environ, ignoreseq=tuple(),
    dumpstride=3, warn_unmapped_labels=True, quiet=True):
    """ Simplistically replace any and all environment-variable-esque
        $VAR_LABEL declarations in :`swaptext` with content from
        appropriate :`swapdic` mappings, *qua* said declared labels. """

    matcher = r'(?<!\\)\${1}([A-Z][A-Z0-9_]+)'
    bracedmatcher = r'(?<!\\)\${1}\{([A-Z][A-Z0-9_]+)\}'
    swapmapper = lambda en: en and (en, swapdic.get(en, "$%s" % en)) or ''
    swapfilter = lambda ex: ex and not (ex in ignoreseq)
    
    envs = dict(map(swapmapper,
        filter(swapfilter,
            re.compile(matcher).findall(swaptext))))
    envs.update(
        dict(map(swapmapper,
            filter(swapfilter,
                re.compile(bracedmatcher).findall(swaptext)))))
    strays = set(envs.keys()).difference(swapdic.keys())

    if warn_unmapped_labels and len(strays) > 0:
        
        for stray in strays:
            print("Warning: unmapped template label %s" % stray,
                file=sys.stderr)
        
        valids = sorted(filter(
            lambda s: s.isupper() and not s.startswith('_'),
                swapdic.keys()), key=len)
        strident = "%%-%ds" % len(list(reversed(valids))[0])
        stride = xrange(0, len(valids), dumpstride)
        
        print("Valid template labels:\n",
            file=sys.stderr)
        for stride in [valids[i:dumpstride+i] for i in stride]:
            print(": ".join(
                [strident % step for step in stride]),
                    file=sys.stderr)

    return Template(
        re.sub(r'(\$+?)(?![A-Z0-9\{]+?)',
            '\g<0>\g<1>', swaptext,
                flags=re.MULTILINE)).safe_substitute(**envs)


def filepath(pth, ignoreseq=tuple(), dumpstride=3,
    warn_unmapped_labels=True, quiet=True):
    """ Perform viron() substitution with file contents. """
    
    try:
        with open(pth, 'r') as filepth:
            return viron(filepth.read(),
                ignoreseq=ignoreseq,
                dumpstride=dumpstride,
                warn_unmapped_labels=warn_unmapped_labels,
                quiet=quiet)
    
    except IOError, err:
        if not quiet:
            print("File path %s is totally invalid" % pth,
                file=sys.stderr)
            print(unicode(err).encode('UTF-8'),
                file=sys.stderr)
        sys.exit(1)


def stdinput(ignoreseq=tuple(), dumpstride=3):
    while 1:
        try:
            line = sys.stdin.readline()
        except KeyboardInterrupt:
            break

        if not line:
            break

        sys.stdout.write(
            viron(line,
                ignoreseq=ignoreseq,
                dumpstride=dumpstride,
                warn_unmapped_labels=False))
    return ''


@arg('FILE', nargs='?', default=None,
    help="File path from which to load text")
@arg('-S', '--dump-stride', default=3,
    help="Number of columns to print when listing valid template labels")
@arg('-i', '--ignore', default="",
    help="Comma-separated list of labels to ignore")
@arg('-v', '--verbose', action='store_true',
    help="Run verbosely")
@arg('-w', '--warn-unmapped-labels', action='store_true',
    help="Issue warnings on STDERR when unknown template labels are encountered")
@arg('-t', '--text', nargs='?', default=None,
    help="Text to process")
def file(args):
    quiet = (not args.verbose)
    warn_unmapped_labels = quiet and False or args.warn_unmapped_labels
    ignoreseq = tuple(str(args.ignore).upper().split(','))
    
    if args.dump_stride < 1:
        warn_unmapped_labels = False
    
    if args.text is None:
    
        if args.FILE is None:
            return stdinput(
                ignoreseq=ignoreseq,
                dumpstride=args.dump_stride)
    
        else:
            
            pth = args.FILE and args.FILE or ''
            if '~' in pth:
                pth = os.path.expanduser(pth)
            if '$' in pth:
                pth = os.path.expandvars(pth)
    
            if not os.path.exists(pth):
                if quiet:
                    print("File path %s is totally invalid" % pth,
                        file=sys.stderr)
                sys.exit(1)
            
            return filepath(pth,
                ignoreseq=ignoreseq,
                dumpstride=args.dump_stride,
                warn_unmapped_labels=warn_unmapped_labels,
                quiet=quiet)
    
    else:
        
        if args.FILE is not None:
            
            pth = args.FILE and args.FILE or ''
            if '~' in pth:
                pth = os.path.expanduser(pth)
            if '$' in pth:
                pth = os.path.expandvars(pth)
    
            if not os.path.exists(pth):
                if quiet:
                    print("File path %s is totally invalid" % pth,
                        file=sys.stderr)
                sys.exit(1)
            
            if not quiet:
                print("Warning: reading from %s (ignoring text '%s')" % (
                    pth, args.text),
                    file=sys.stderr)
            return filepath(pth,
                ignoreseq=ignoreseq,
                dumpstride=args.dump_stride,
                quiet=quiet)
    
        else:
            return viron(args.text,
                ignoreseq=ignoreseq,
                dumpstride=args.dump_stride,
                warn_unmapped_labels=warn_unmapped_labels,
                quiet=quiet)


p = ArghParser()
p.add_commands([file, filepath, viron])

def main(argv=None):
    argv = list(argv and argv or sys.argv[1:])
    #print(argv)
    
    cmdarg = argv[0:1]
    if len(cmdarg) > 0:
        cmd = cmdarg[0]
    else:
        cmd = None
    
    if cmd is not None and cmd not in ('file', 'filepath'):
        argv.insert(0, 'file')
    
    p.dispatch(argv=argv)

if __name__ == "__main__":
    main()
    sys.exit(0)

