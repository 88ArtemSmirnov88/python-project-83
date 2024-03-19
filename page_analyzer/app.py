import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
connection = psycopg2.connect(DATABASE_URL)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/urls', methods=['POST'])
def post_urls():
    url = request.form['url']
    errors = validate(url)
    if errors:
        return render_template('home.html')
    with connection.cursor() as cursor:
        cursor.execute(
            'insert into urls (name, created_at) values (%s, %s) returning id;',
            (url, datetime.now())
        )
        id = cursor.fetchone().id
    connection.commit()
    connection.close()
    return redirect(url_for('url_show', id=id))


def validate(url):
    errors = []
    if len(url) > 255:
        errors.append('url превышает 255 символов')
    return errors

@app.route('/urls/<id>')
def url_show(id):
    with connection.cursor() as cursore:
        cursore.execute(
            'select * from urls where id = %s', (id,)
        )
        url = cursore.fetchone()
    connection.commit()
    connection.close()
    return render_template('url.html', url=url)