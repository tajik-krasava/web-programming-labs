from flask import Flask, redirect, url_for, render_template
from lab1 import lab1

app = Flask(__name__)
app.register_blueprint(lab1)

@app.route("/")
def go():
    return redirect("/menu", code=302)


@app.route("/index")
def start():
    return redirect("/menu", code=302)


@app.route("/menu")
def menu():
    return """
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body> 
        <header>
            НГТУ, ФБ, Лабораторные работы
        </header>
<h1>Web-сервер на Flask</h1>
    <ul>
        <li><a href="/lab1">Лабораторная работа 1</a></li>
        <li><a href="/lab2">Лабораторная работа 2</a></li>
    </ul>
        <footer>
            &copy; Игорь Богачев, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
"""

@app.route('/lab2/example')
def example():
    name, lab, group, course = 'Богачев Игорь', 2, 'ФБИ-23', '3 курс'
    fruits = [{'name': 'яблоки', 'price': 100},
              {'name': 'груши', 'price': 120},
              {'name': 'апельсины', 'price': 80},
              {'name': 'мандарины', 'price': 95},
              {'name': 'манго', 'price': 321}
              ]
    books = [{'author': 'Шарлотта Бронте', 'name': 'Джейн Эйр', 'genre': 'роман', 'pages': 630},
             {'author': 'Рэй Брэдбери', 'name': '451 градус по Фаренгейту',
                 'genre': 'роман-антиутопия', 'pages': 256},
             {'author': 'Джон Р. Р. Толкин', 'name': 'Хоббит, или Туда и обратно',
                 'genre': 'повесть', 'pages': 320},
             {'author': 'Луиза Мэй Олкотт', 'name': 'Маленькие женщины',
                 'genre': 'роман', 'pages': 883},
             {'author': 'Элвин Брукс Уайт', 'name': 'Паутина Шаролтты',
                 'genre': 'детская книга', 'pages': 240},
             {'author': 'Фрэнсис Скотт Фицджеральд',
                 'name': 'Великий Гэтсби', 'genre': 'роман', 'pages': 256},
             {'author': 'Джордж Оруэлл', 'name': '1984',
                 'genre': 'роман-антиутопия', 'pages': 328},
             {'author': 'Анна Франк', 'name': 'Дневник Анны Франк',
                 'genre': 'дневник', 'pages': 512},
             {'author': 'Джейн Остин', 'name': 'Гордость и предубеждение',
                 'genre': 'роман', 'pages': 567},
             {'author': 'Харпер Ли', 'name': 'Убить пересмешника',
                 'genre': 'роман', 'pages': 374}
             ]
    return render_template('example.html',
                           fruits=fruits,
                           books=books,
                           name=name,
                           lab=lab,
                           group=group,
                           course=course,)


@app.route('/lab2/')
def lab():
    return render_template('lab2.html')


@app.route('/lab2/top_fighters_k1')
def fighters():
    return render_template('top_fighters_k1.html')
