# -*- coding: utf-8 -*-
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World!"

@app.route('/test')
def index_test():
    return "Hello World test!"

if __name__ == '__main__':
    app.run()
