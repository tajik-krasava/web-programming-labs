from flask import Blueprint, render_template, request, redirect, session, flash
import psycopg2
from psycopg2.extras import RealDictCursor

lab5 = Blueprint('lab5', __name__)


@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))

def db_connect():
    conn = psycopg2.connect(dbname="igor_bogachev_knowledge_base", user="postgres", password="admin", host="127.0.0.1")
    cur = conn.cursor(cursor_factory = RealDictCursor)
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab5.route('/lab5/list')
def list_articles():
    return 'Страница со списком статей'


@lab5.route('/lab5/create')
def create_article():
    return 'Страница для создания статей'


@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    login = request.form.get('login')
    password = request.form.get('password')
    if not (login or password):
        return render_template('lab5/login.html', error="Заполните поля")

    if not (login and password):
        return render_template('lab5/login.html', error="Заполните поля")

    conn, cur = db_connect()

    cur.execute("SELECT * FROM users WHERE login=%s", (login,))
    user = cur.fetchone()

    if not user or user['password'] != password:
        return render_template('lab5/login.html',
                               error='Логин и/или пароль неверны')

    if user['password'] != password:
        cur.close()
        conn.close()
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')

    session['login'] = login
    cur.close()
    conn.close()
    return render_template('lab5/success_login.html')


@lab5.route('/lab5/success_login')
def success_login():
    return render_template('lab5/success_login.html')


@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')
    if not (login or password):
        return render_template('lab5/register.html', error='Заполните все поля')

    conn, cur = db_connect()

    cur.execute(f"SELECT login FROM users WHERE login='{login}'")
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html', error='Такой пользователь уже существует')

    cur.execute(f"INSERT INTO users (login, password) VALUES ('{login}', '{password}')")

    db_close(conn, cur)
    return render_template('lab5/success.html', login=login)


@lab5.route('/lab5/success')
def success():
    return render_template('lab5/success.html')