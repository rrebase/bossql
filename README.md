# bossql

A Software Engineering Project.

Learn SQL through challenges.

Dev setup
---------

Create a `local_settings.py` file in 
the root directory of the project.
Create corresponding database users
and databases.

Example:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'bossql_dev',
        'USER': 'bacon',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

ENV_DATABASE = {
    'dbname': 'bossql_env',
    'user': 'bossql',
    'password': 'bossql',
}
```

Run migrations with
`python3 manage.py migrate`

Start the development server with
`python3 manage.py runserver`


Python coding style
-------------------

Changes to bossql Python code should conform to
PEP8 style guide.