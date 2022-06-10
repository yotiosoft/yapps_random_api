# -*- coding: utf-8 -*-
import sys
from flask import Flask, request
import random

app = Flask(__name__)


class query_class:
    def __init__(self):
        self.min = 0
        self.max = 0
        self.mu = 0
        self.sigma = 0
        self.mode = 0
        self.lambd = 0.0
        self.alpha = 0.0
        self.beta = 0.0
        self.type = ""

    def get(self, distribution):
        try:
            self.type = request.args.get("type")
            if self.type is None:
                self.type = "int"
            else:
                if self.type != "float" and self.type != "int":
                    self.type = "int"
                    
            if distribution == "uniform" or distribution == "triangular":
                req_min = request.args.get("min")
                req_max = request.args.get("max")

                if self.type == "int":
                    if req_min is None:
                        self.min = -sys.maxsize
                    else:
                        self.min = int(req_min)
                    
                    if req_max is None:
                        self.max = sys.maxsize
                    else:
                        self.max = int(req_max)
                else:
                    if req_min is None:
                        self.min = sys.float_info.min
                    else:
                        self.min = float(req_min)
                    
                    if req_max is None:
                        self.max = sys.float_info.max
                    else:
                        self.max = float(req_max)

                if distribution == "triangular":
                    req_mode = request.args.get("mode")
                    if req_mode is None:
                        self.mode = (self.min+self.max)/2
                    else:
                        self.mode = int(req_mode)
                        
                return

            elif distribution == "normal":
                req_mu = request.args.get("mu")
                req_sigma = request.args.get("sigma")

                if req_mu is None:
                    self.mu = 0
                else:
                    self.mu = int(req_mu)
                
                if req_sigma is None:
                    self.sigma = 1
                else:
                    self.sigma = int(req_sigma)
                return

            elif distribution == "lambda":
                req_lambd = request.args.get("lambd")

                if req_lambd is None:
                    self.lambd = 1
                else:
                    self.lambd = 1/float(req_lambd)
                return

            elif distribution == "beta" or distribution == "gamma":
                req_alpha = request.args.get("alpha")
                req_beta = request.args.get("beta")

                if req_alpha is None:
                    self.alpha = 1.0
                else:
                    self.alpha = int(req_alpha)
                
                if req_beta is None:
                    self.beta = 2.0
                else:
                    self.beta = int(req_beta)
                return
        except ValueError:
            return "Error: 引数が正しくありません"


@app.route('/')
def root_index():
    return "Successfully accessed."

@app.route('/uniform', methods=["GET"])
def uniform_index():
    query = query_class()
    query.get("uniform")

    try:
        if query.type == "int":
            rand = str(random.randint(query.min, query.max))
        else:
            rand = random.uniform(query.min, query.max)
    except ValueError:
        return "Error: 正しいパラメータが指定されていません"

    return str(rand)

@app.route('/normal', methods=["GET"])
def normal_index():
    query = query_class()
    query.get("normal")

    try:
        rand = random.gauss(query.mu, query.sigma)
        if query.type == "int":
            rand = int(rand)
    except ValueError:
        return "Error: 正しいパラメータが指定されていません"

    return str(rand)

@app.route('/beta', methods=["GET"])
def beta_index():
    query = query_class()
    query.get("beta")

    try:
        rand = random.betavariate(query.alpha, query.beta)
        if query.type == "int":
            rand = int(rand)
    except ValueError:
        return "Error: 正しいパラメータが指定されていません"

    return str(rand)

@app.route('/triangular', methods=["GET"])
def triangular_index():
    query = query_class()
    query.get("triangular")

    try:
        rand = random.triangular(query.min, query.max, query.mode)
        if query.type == "int":
            rand = int(rand)
    except ValueError:
        return "Error: 正しいパラメータが指定されていません"

    return str(rand)

@app.route('/lambda', methods=["GET"])
def lambda_index():
    query = query_class()
    query.get("lambda")

    try:
        rand = random.expovariate(query.lambd)
        if query.type == "int":
            rand = int(rand)
    except ValueError:
        return "Error: 正しいパラメータが指定されていません"

    return str(rand)

@app.route('/gamma', methods=["GET"])
def gamma_index():
    query = query_class()
    query.get("gamma")

    try:
        rand = random.gammavariate(query.alpha, query.beta)
        if query.type == "int":
            rand = int(rand)
    except ValueError:
        return "Error: 正しいパラメータが指定されていません"

    return str(rand)

if __name__ == '__main__':
    app.run()
