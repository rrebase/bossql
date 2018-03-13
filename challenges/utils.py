import psycopg2

from django.conf import settings

def get_env_db_conn():
    return psycopg2.connect(**settings.ENV_DATABASE)
