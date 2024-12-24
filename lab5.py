from flask import Blueprint, render_template, request, redirect, session, flash
import psycopg2
from psycopg2.extras import RealDictCursor

lab5 = Blueprint('lab5', __name__)


@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))


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

    conn = psycopg2.connect(dbname="igor_bogachev_knowledge_base", user="postgres", password="admin", host="127.0.0.1"
                            )
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(f"SELECT * FROM users WHERE login='{login}'")
    user = cur.fetchone()

    if not user:
        cur.close()
        conn.close()
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
    if not (login and password):
        return render_template('lab5/register.html', error="Заполните все поля")

    try:
        conn = psycopg2.connect(dbname="igor_bogachev_knowledge_base",
                                user="postgres", password="admin", host="127.0.0.1")
        cur = conn.cursor()
        cur.execute("SELECT login FROM users WHERE login=%s", (login,))
        if cur.fetchone():
            cur.close()
            conn.close()
            return render_template('lab5/register.html', error="Такой пользователь уже существует")

        cur.execute(
            "INSERT INTO users (login, password) VALUES (%s, %s);", (login, password))
        conn.commit()
    except Exception as e:
        return render_template('lab5/register.html', error="Произошла ошибка при регистрации: " + str(e))

    finally:
        cur.close()
        conn.close()

        return render_template('lab5/success.html', login=login)


@lab5.route('/lab5/success')
def success():
    return render_template('lab5/success.html')
