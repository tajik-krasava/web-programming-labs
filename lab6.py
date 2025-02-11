from flask import Blueprint,render_template,request, redirect, session, current_app
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path
from dotenv import load_dotenv
import psycopg2
lab6 = Blueprint('lab6',__name__)

@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')



load_dotenv()


def db_connect():
    if current_app.config['DB_TYPE']=='postgres':
        conn=psycopg2.connect(
            host = '127.0.0.1',
            database = 'egor_lapshin_knowledge_base',
            user = 'egor_lapshin_knowledge_base',
            password = '123',
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

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']

    if data['method'] == 'info':
        conn,cursor = db_connect()
        cursor.execute('SELECT * FROM offices')
        offices = cursor.fetchall()
        db_close(conn, cursor)
        return {
            'jsonrpc': '2.0',
            'result': [dict(office) for office in offices],
            'id': id
        }

    login = session.get('login')
    if not login:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Unauthorized'
            },
            'id': id
        }

    if data['method'] == 'booking':
        office_number = data['params']
        conn,cursor = db_connect()
        if current_app.config['DB_TYPE'] == 'postgres':
            cursor.execute('SELECT * FROM offices WHERE number = %s;', (office_number,))
        else:
            cursor.execute('SELECT * FROM offices WHERE number = ?;', (office_number,))
        office = cursor.fetchone()
        if not office:
            db_close(conn, cursor)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 3,
                    'message': 'Office not found'
                },
                'id': id
            }
        if office['tenant']:
            db_close(conn, cursor)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 2,
                    'message': 'Already booked'
                },
                'id': id
            }
        if current_app.config['DB_TYPE'] == 'postgres':
            cursor.execute('UPDATE offices SET tenant = %s WHERE number = %s;', (login, office_number))
        else:
            cursor.execute('UPDATE offices SET tenant = ? WHERE number = ?;', (login, office_number))
        db_close(conn, cursor)
        return {
            'jsonrpc': '2.0',
            'result': 'success',
            'id': id
        }

    if data['method'] == 'cancellation':
        office_number = data['params']
        conn,cursor = db_connect()
        if current_app.config['DB_TYPE'] == 'postgres':
            cursor.execute('SELECT * FROM offices WHERE number = %s', (office_number,))
        else:
            cursor.execute('SELECT * FROM offices WHERE number = ?;', (office_number,))
        office = cursor.fetchone()
        if not office:
            db_close(conn, cursor)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 3,
                    'message': 'Office not found'
                },
                'id': id
            }
        if not office['tenant']:
            db_close(conn, cursor)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 4,
                    'message': 'Office not booked'
                },
                'id': id
            }
        if office['tenant'] != login:
            db_close(conn, cursor)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 5,
                    'message': 'Not your booking'
                },
                'id': id
            }
        if current_app.config['DB_TYPE'] == 'postgres':
            cursor.execute('UPDATE offices SET tenant = NULL WHERE number = %s;', (office_number,))
        else:
            cursor.execute('UPDATE offices SET tenant = NULL WHERE number = ?;', (office_number,))
        db_close(conn, cursor)
        return {
            'jsonrpc': '2.0',
            'result': 'success',
            'id': id
        }

    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }