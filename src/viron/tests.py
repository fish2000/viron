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

separators = 70
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

if __name__ == "__main__":
    
    import tempfile
    from viron import main as viron
    
    # passing text
    #viron(['--text', yodogg])
    print("PASSING TEXT")
    print("=" * separators)
    
    viron(['-t', yodogg])
    
    print("-" * separators)
    print('')
    print('')
    
    # passing path to text in file
    print("PASSING PATH TO TEXT")
    print("=" * separators)
    
    tmp_name = "%s-PATH-TO-TEXT.txt" % tempfile.mktemp()
    with open(tmp_name, "w+b") as tmp:
        tmp.write(yodogg)
    viron([tmp_name])
    
    print("-" * separators)
    print('')
    print('')
    
    # passing invalid path
    print("PASSING INVALID PATH")
    print("=" * separators)
    
    bad_tmp_name = "%s-BAD-PATH" % tempfile.mktemp()
    viron([bad_tmp_name])
    
    print("-" * separators)
    print('')
    print('')
    