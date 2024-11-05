# app.py
import webview
from flask import Flask, render_template_string
 
app = Flask(__name__)
 
@app.route('/')
def index():
    return render_template_string('''
    <!doctype html>
    <html>
    <head>
        <style>
            body { font-family: Arial; }
            button { background-color: lightblue; color: black; padding: 10px; }
        </style>
    </head>
    <body>
        <h1>Hello, World!</h1>
        <button onclick="alert('Button clicked!')">Cliquez ici</button>
        <form><input type="text"></form>
    </body>
    </html>
    ''')
 
 
 
if __name__ == '__main__':
    webview.create_window('Mon application', app)
    webview.start()