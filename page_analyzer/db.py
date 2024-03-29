import os
from dotenv import load_dotenv
import psycopg2
from datetime import datetime
from psycopg2.extras import NamedTupleCursor

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

def connect_to_db():
    return psycopg2.connect(DATABASE_URL)

def insert_url(connect, url):
    with connect.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute(
            'insert into urls (name, created_at) values (%s, %s) returning id;',
            (url, datetime.now())
        )
        id = cursor.fetchone().id
    return id

def get_url_by_id(connect, id):
    with connect.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute(
            'select * from urls where id = %s', (id,)
        )
        url = cursor.fetchone()
    return url

def get_url_by_name(connect, url):
    with connect.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute(
            'select id, name from urls where name = %s', (url,)
        )
        url = cursor.fetchone()
    return url
