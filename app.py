from flask import Flask, redirect, url_for, render_template
from lab1 import lab1
from lab2 import lab2 
from lab3 import lab3

app = Flask(__name__)
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)

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
        <li><a href="/lab3">Лабораторная работа 3</a></li>
    </ul>
        <footer>
            &copy; Игорь Богачев, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
"""

