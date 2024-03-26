from page_analyzer import db
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


def validate(url):
    errors = []
    if len(url) > 255:
        errors.append('url превышает 255 символов')
    return errors

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/urls', methods=['POST'])
def post_urls():
    connect = db.connect_to_db()
    url = request.form['url']
    errors = validate(url)
    if errors:
        return render_template('home.html')
    url = db.get_url_by_name(connect, url)
    if url:
        id = url.id
        flash('Страница уже существует', 'info')
    else:
        id = db.insert_url(connect, url)
        connect.commit()
        flash('Страница успешно добавлена', 'success')
    connect.close()
    return redirect(url_for('url_show', id=id))

@app.route('/urls/<id>')
def url_show(id):
    connect = db.connect_to_db()
    url = db.get_url_by_id(connect, id)
    connect.commit()
    connect.close()
    return render_template('url.html', url=url)