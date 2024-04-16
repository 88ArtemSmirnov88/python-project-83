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
            'select * from urls where id = %s order by created_at desc', (id,)
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

def get_urls(connect):
    with connect.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute(
            'select u.id, name, uc.created_at, uc.status_code from urls u left join url_checks uc on u.id = uc.url_id order by created_at desc;'
        )
        urls = cursor.fetchall()
    return urls

def insert_url_checks(connect, id, status_code, page_data):
    with connect.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute(
            'insert into url_checks (url_id, status_code, h1, title, description, created_at) values (%s, %s, %s, %s, %s, %s);',
            (id, status_code, page_data['h1'], page_data['title'], page_data['description'], datetime.now())
        )

def get_url_checks(connect, id):
    with connect.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute(
            'select * from url_checks where url_id = %s order by created_at desc;',
            (id,)
        )
        url_checks = cursor.fetchall()
    return url_checks
