# utils/db.py

import psycopg2
from psycopg2 import pool
from config import Config

connection_pool = None


def init_db_pool():
    global connection_pool
    connection_pool = psycopg2.pool.SimpleConnectionPool(
        1,
        10,
        Config.DATABASE_URL
    )


def get_connection():
    if connection_pool is None:
        init_db_pool()
    connection = connection_pool.getconn()
    return connection


def release_connection(connection):
    connection_pool.putconn(connection)