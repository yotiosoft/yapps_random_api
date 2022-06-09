# -*- coding: utf-8 -*-
from flask import Flask
import numpy

main = Flask(__name__)

@main.route('/')
def index():
    return "Hello World!"

if __name__ == '__main__':
    main.run()
