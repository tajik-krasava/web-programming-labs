from flask import Blueprint, url_for, redirect, render_template, request, make_response
lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    return render_template('lab3/lab3.html', name=name, name_color=name_color)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'
    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    background_color = request.args.get('background-color')
    font_size = request.args.get('font-size')
    if color:
        resp = make_response(redirect('/lab3/settings'))
        resp.set_cookie('color', color)
        resp.set_cookie('background-color', background_color)
        resp.set_cookie('font-size', font_size)
        return resp
    color = request.cookies.get('color')
    background_color = request.cookies.get('background-color')
    font_size = request.cookies.get('font-size')
    resp = make_response(render_template('lab3/settings.html', color=color, background_color=background_color, font_size=font_size))
    return resp

@lab3.route('/lab3/del_settings')
def del_settings():
    resp = make_response(redirect('/lab3/settings'))
    cookies = request.cookies.keys()
    for cookie in cookies:
        resp.set_cookie(cookie, '', expires=0)
    return resp