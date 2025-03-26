from main import app
from flask import Flask, render_template

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dynamic/<string:name>')
def dynmic(name):
    print(name)
    return render_template('home2.html',name = name)

@app.route('/about')
def about():
    return "About the site."