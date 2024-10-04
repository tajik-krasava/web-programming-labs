from flask import Flask, redirect, url_for, render_template
app = Flask(__name__)


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


@app.route("/lab1")
def lab1():
    return """
<!doctype html>
<html>
    <head>
        <title>Богачев Игорь Андреевич, лабораторная 1</title>
    </head>
    <body> 
        <header>
            НГТУ, ФБ, Лабораторная работа 1
        </header>

        <h1>web-сервер на flask</h1>
        
        <p>Flask — фреймворк для создания веб-приложений на языке
программирования Python, использующий набор инструментов
Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
называемых микрофреймворков — минималистичных каркасов веб-приложений, сознательно предоставляющих лишь самые ба-
зовые возможности.
<a href="/menu">Меню</a></li>
<h2>Реализованные роуты</h2>
    <ul>
        <li><a href="/lab1">lab1</a></li>
        <li><a href="/lab1/oak">lab1/oak - дуб</a></li>
        <li><a href="/lab1/student">lab1/student - студент</a></li>
        <li><a href="/lab1/python">lab1/python - python</a></li>
    </ul>
        <footer>
            &copy; Игорь Богачев, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
"""


@app.route("/lab1/oak")
def oak():
    return '''
<!doctype html>
<html>
    <body> 
      <h1>Дуб</h1>
      <img src="''' + url_for('static', filename='oak.jpg') + '''">
      <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') + '''">  
    </body>
    <footer>
            &copy; Игорь Богачев, ФБИ-23, 3 курс, 2024
        </footer>
</html>
'''


@app.route("/lab1/student")
def lab1s():
    return '''
<!doctype html>
<html>
    <head>
        <title>Богачев Игорь Андреевич</title>
    </head>
    <body>
        <h1>Богачев Игорь Андреевич</h1>
        <img src="''' + url_for('static', filename='nstu.png') + '''">
    </body>
    <footer>
            &copy; Игорь Богачев, ФБИ-23, 3 курс, 2024
        </footer>
</html>
'''


@app.route("/lab1/python")
def lab1python():
    return '''
<!doctype html>
<html>
    <head>
        <title>Богачев Игорь Андреевич, лабораторная 1</title>
    </head>
    <body> 
        <header>
            НГТУ, ФБ, Лабораторная работа 1
        </header>

        <h1>Python</h1>
        
            <p>Python — это высокоуровневый язык программирования, отличающийся эффективностью, простотой и универсальностью использования. 
            Он широко применяется в разработке веб-приложений и прикладного программного обеспечения, а также в машинном обучении и обработке больших данных. 
            За счет простого и интуитивно понятного синтаксиса является одним из распространенных языков для обучения программированию. 
        <h2>История разработки и названия</h2>
            <p>Язык программирования Python был создан в 1989–1991 годах голландским программистом Гвидо ван Россумом. 
            Изначально это был любительский проект: разработчик начал работу над ним, просто чтобы занять себя на рождественских каникулах. 
            Хотя сама идея создания нового языка появилась у него двумя годами ранее. 
            Имя ему Гвидо взял из своей любимой развлекательной передачи «Летающий цирк Монти Пайтона». 
            Язык программирования он и выбрал — Python, что это означало название комик-группы. 
            Это шоу было весьма популярным среди программистов, которые находили в нем параллели с миром компьютерных технологий.
        <img src="''' + url_for('static', filename='python.jpg') + '''">
        <footer>
            &copy; Игорь Богачев, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
'''


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
    return render_template('top.html')
