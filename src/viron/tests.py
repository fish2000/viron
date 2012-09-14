
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
    import sys
    sys.argv = ['viron', yodogg]
    from viron import main
    main()
    