from flask import Blueprint, render_template, request, abort, jsonify, current_app
from os import path
import sqlite3
from datetime import datetime
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path
from dotenv import load_dotenv
import psycopg2
lab7 = Blueprint('lab7', __name__)

def db_connect():
    if current_app.config['DB_TYPE']=='postgres':
        conn=psycopg2.connect(
            host = '127.0.0.1',
            database = 'WEB',
            user = 'postgres',
            password = 'postgres',
            port=5432
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn, cur = db_connect()
    cur.execute('SELECT * FROM films')
    films = cur.fetchall()
    db_close(conn, cur)
    return jsonify([dict(film) for film in films])

films = []



@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute('SELECT * FROM films WHERE id = %s', (id,))
    else:
        cur.execute('SELECT * FROM films WHERE id = ?', (id,))
    film = cur.fetchone()
    db_close(conn, cur)
    if film is None:
        abort(404, description="Film not found")
    return jsonify(dict(film))

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute('DELETE FROM films WHERE id = %s', (id,))
    else:
        cur.execute('DELETE FROM films WHERE id = ?', (id,))
    db_close(conn, cur)
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    film = request.get_json()
    errors = validate_film(film)
    if errors:
        return jsonify(errors), 400

    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute('UPDATE films SET title = %s, title_ru = %s, year = %s, description = %s WHERE id = %s',
                    (film['title'], film['title_ru'], film['year'], film['description'], id))
    else:
        cur.execute('UPDATE films SET title = ?, title_ru = ?, year = ?, description = ? WHERE id = ?',
                    (film['title'], film['title_ru'], film['year'], film['description'], id))
    db_close(conn, cur)
    return jsonify(film)

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    new_film = request.get_json()
    errors = validate_film(new_film)
    if errors:
        return jsonify(errors), 400

    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute('INSERT INTO films (title, title_ru, year, description) VALUES (%s, %s, %s, %s)',
                    (new_film['title'], new_film['title_ru'], new_film['year'], new_film['description']))
    else:
        cur.execute('INSERT INTO films (title, title_ru, year, description) VALUES (?, ?, ?, ?)',
                (new_film['title'], new_film['title_ru'], new_film['year'], new_film['description']))
    new_film['id'] = cur.lastrowid
    db_close(conn, cur)
    return jsonify(new_film), 201


def validate_film(film):
    errors = {}
    current_year = datetime.now().year

    if not film.get('title') and not film.get('title_ru'):
        errors['title'] = 'Название на оригинальном языке или русское название должно быть заполнено'

    if not film.get('title_ru'):
        errors['title_ru'] = 'Русское название должно быть заполнено'

      # Преобразуем значение в число
    if not (1895 <= int(film.get('year', 0))):
        errors['year'] = f'Год должен быть от 1895 до {current_year}'

    if not film.get('description'):
        errors['description'] = 'Описание должно быть заполнено'
    elif len(film.get('description', '')) > 2000:
        errors['description'] = 'Описание должно быть не более 2000 символов'

    return errors