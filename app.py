from flask import Flask, redirect, url_for
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
            НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
        </header>

        <ul>
        <li><a href="/lab1">lab1</a></li>
        </ul>

        <footer>
            &copy; Игорь Богачев, ФБИ-23, 3 курс, 2023
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

        <footer>
            &copy; Игорь Богачев, ФБИ-23, 3 курс, 2023
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
</html>
'''