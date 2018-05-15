from contextlib import contextmanager

import psycopg2

from django.conf import settings


def get_env_db_conn():
    return psycopg2.connect(**settings.ENV_DATABASE)


@contextmanager
def get_env_db_cur():
    with get_env_db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("DROP SCHEMA IF EXISTS bossql_env CASCADE;")
            cur.execute("CREATE SCHEMA bossql_env;")
            yield cur
            conn.rollback()
