from flask import Blueprint, url_for, redirect
lab1 = Blueprint('lab1', __name__)


@lab1.route("/lab1")
def lab():
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


@lab1.route("/lab1/oak")
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


@lab1.route("/lab1/student")
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
        <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') + '''">
    </body>
    <footer>
            &copy; Игорь Богачев, ФБИ-23, 3 курс, 2024
        </footer>
</html>
'''


@lab1.route("/lab1/python")
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
        <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') + '''">
    </body>
    <footer>
            &copy; Игорь Богачев, ФБИ-23, 3 курс, 2024
    </footer>
</html>
'''
