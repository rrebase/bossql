import psycopg2

from django.conf import settings

def get_env_db_conn():
<<<<<<< HEAD
    return psycopg2.connect("dbname=bossql_env user=rareba password=UnrealhfK9")
=======
    return psycopg2.connect(**settings.ENV_DATABASE)
>>>>>>> 0fe0fcb444556672bfb39cf2cd08bc4332165887
