from flask import Blueprint, render_template, request, redirect, session, flash
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
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
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    conn, cur = db_connect()
    cur.execute(f"SELECT id FROM users WHERE login='{login}'")
    user_id = cur.fetchone()["id"]

    cur.execute(f"SELECT * FROM aricles WHERE user_id='{user_id}';")
    articles = cur.fetchall()

    db_close(conn, cur)
    return render_template('/lab5/articles.html', articles=articles)


@lab5.route('/lab5/create', methods = ['GET', 'POST'])
def create_article():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    if request.method == 'GET':
        return render_template('lab5/create.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')

    conn, cur = db_connect()

    cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    login_id = cur.fetchone()["id"]

    cur.execute(f"INSERT INTO aricles(user_id, title, article_text) VALUES ({login_id}, '{title}', '{article_text}')")

    db_close(conn, cur)
    return redirect('/lab5')


@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('lab5/login.html', error="Заполните поля")

    conn, cur = db_connect()

    cur.execute("SELECT * FROM users WHERE login=%s", (login,))
    user = cur.fetchone()

    if not check_password_hash(user['password'], password):
        db_close(conn,cur)
        return render_template('lab5/login.html',
                               error='Логин и/или пароль неверны')

    session['login'] = login
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

    password_hash = generate_password_hash(password)
    cur.execute(f"INSERT INTO users (login, password) VALUES ('{login}', '{password_hash}')")

    db_close(conn, cur)
    return render_template('lab5/success.html', login=login)

@lab5.route('/lab5/success')
def success():
    return render_template('lab5/success.html')
