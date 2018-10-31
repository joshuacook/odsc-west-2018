import psycopg2 as pg2
from pandas import DataFrame
from psycopg2.extras import RealDictCursor

HOST = "this_postgres"
USER = "postgres"
DATABASE = "postgres"

def connect_to_db():
    con = pg2.connect(host=HOST,
                      dbname=DATABASE,
                      user=USER)
    cur = con.cursor(cursor_factory=RealDictCursor)
    return con, cur

def query_database(query, fetch_res=True):
    con, cur = connect_to_db()
    cur.execute(query)
    if fetch_res:
        results = cur.fetchall()
    else:
        results = None
    con.close()
    return results

def query_to_dataframe(query):
    return DataFrame(query_database(query))
