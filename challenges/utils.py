import psycopg2

def get_env_db_conn():
    return psycopg2.connect("dbname=bossql_env user=rareba password=UnrealhfK9")