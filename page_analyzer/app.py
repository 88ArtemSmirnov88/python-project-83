import os
import requests
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from datetime import datetime
from page_analyzer import parser
from page_analyzer import validator
from page_analyzer import db

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/urls', methods=['POST'])
def post_urls():
    connect = db.connect_to_db()
    url = request.form['url']
    errors = validator.validate(url)
    if errors:
        return render_template('home.html')
    
    normalized_url = validator.normalize(url)
    existed_url = db.get_url_by_name(connect, normalized_url)
    if existed_url:
        id = existed_url.id
        flash('Страница уже существует', 'info')
    else:
        id = db.insert_url(connect, normalized_url)
        connect.commit()
        flash('Страница успешно добавлена', 'success')
    connect.close()
    return redirect(url_for('url_show', id=id))

@app.route('/urls/<id>')
def url_show(id):
    connect = db.connect_to_db()
    url = db.get_url_by_id(connect, id)
    connect.commit()
    url_checks = db.get_url_checks(connect, id)
    connect.commit()
    connect.close()
    return render_template('url.html', url=url, url_checks=url_checks)

@app.route('/urls')
def urls_show():
    connect = db.connect_to_db()
    urls = db.get_urls(connect)
    connect.commit()
    connect.close()
    return render_template('urls.html', urls=urls)

@app.post('/urls/<id>/checks')
def url_checks(id):
    connect = db.connect_to_db()
    url = db.get_url_by_id(connect, id)
    connect.commit()

    try:
        response = requests.get(url.name)
        status_code = response.status_code
        response.raise_for_status()
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке.', 'danger')
        return redirect(url_for('url_show', id=id))
    
    page_data = parser.get_page_data(response)
    db.insert_url_checks(connect, id, status_code, page_data)
    connect.commit()
    connect.close()
    flash('Страница успешно проверена.', 'success')
    return redirect(url_for('url_show', id=id))
    