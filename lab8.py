from flask import Blueprint, render_template, request, redirect, session, flash, current_app, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user
import sqlite3

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab():
    return render_template('lab8/lab8.html', login=session.get('login'))

@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember = request.form.get('remember')

    if not login_form:
        return render_template('lab8/login.html', error='Имя пользователя не должно быть пустым')
    
    if not password_form:
        return render_template('lab8/login.html', error='Пароль не должен быть пустым')

    user = users.query.filter_by(login = login_form).first()

    if user:
        if check_password_hash(user.password, password_form):
            login_user(user, remember = remember)
            return redirect('/lab8/')
        
    return render_template('/lab8/login.html', error = 'Ошибка входа: логин и/или пароль неверный')

@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form:
        return render_template('lab8/register.html', error='Имя пользователя не должно быть пустым')
    
    if not password_form:
        return render_template('lab8/register.html', error='Пароль не должен быть пустым')


    login_exists = users.query.filter_by(login = login_form).first()
    if login_exists:
        return render_template('lab8/register.html', error = 'Такой пользователь уже существует')
    
    password_hash = generate_password_hash (password_form)
    new_user =  users(login = login_form, password = password_hash)
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user, remember=False)
    flash('Вы успешно зарегистрированы и вошли в систему!', 'success')
    return redirect('/lab8/')

@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    session.pop('login', None)
    return redirect('/lab8/')

@lab8.route('/lab8/list', methods=['GET'])
@login_required
def list_articles():
    articles = articles.query.all()
    return render_template('lab8/articles.html', articles=articles)

@lab8.route('/lab8/articles/create', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = request.form.get('is_public')

    if not title or not article_text:
        flash('Название и содержание статьи не должны быть пустыми', 'error')
        return redirect(url_for('lab8.list_articles'))

    new_article = articles(title=title, article_text=article_text,is_public=is_public, login_id=current_user.id)
    db.session.add(new_article)
    db.session.commit()
    flash('Статья успешно создана!', 'success')
    return redirect(url_for('lab8.list_articles')) 

@lab8.route('/lab8/articles/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.get_or_404(article_id)

    if article.login_id != current_user.id:
        flash('У вас нет прав для редактирования этой статьи', 'error')
        return redirect('/lab8/list')

    if request.method == 'GET':
        return render_template('lab8/edit_article.html', article=article)

    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = request.form.get('is_public')

    if not title or not article_text:
        flash('Название и содержание статьи не должны быть пустыми', 'error')
        return redirect(url_for('lab8.edit_article', article_id=article_id))

    article.title = title
    article.article_text = article_text
    article.is_public = True if is_public == 'on' else False
    db.session.commit()
    flash('Статья успешно обновлена!', 'success')
    return redirect('/lab8/list')

@lab8.route('/lab8/articles/delete/<int:article_id>', methods=['POST'])
@login_required
def delete_article(article_id):
    article = articles.query.get_or_404(article_id)

    if article.login_id != current_user.id:
        flash('У вас нет прав для удаления этой статьи', 'error')
        return redirect('/lab8/list')

    db.session.delete(article)
    db.session.commit()
    flash('Статья успешно удалена!', 'success')
    return redirect('/lab8/list')


@lab8.route('/lab8/public_articles', methods=['GET'])
def list_public_articles():
    articles = articles.query.filter_by(is_public=True).all()
    return render_template('lab8/public_articles.html', articles=articles) 

@lab8.route('/lab8/articles/search', methods=['GET'])
def search_articles():
    query = request.args.get('q')
    if query:
 
        articles = articles.query.filter(
            (articles.title.ilike(f'%{query}%')) | 
            (articles.article_text.ilike(f'%{query}%'))
        ).all()
    else:
        articles = []

    return render_template('lab8/search_results.html', articles=articles)