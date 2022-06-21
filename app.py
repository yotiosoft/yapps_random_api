# -*- coding: utf-8 -*-
import sys
from flask import Flask, request
from flask_cors import CORS
import random
import json

app = Flask(__name__)

# 別サーバ(=GitHub Pages)からのリクエストを許可
CORS(app, supports_credentials=True)

jrand = {}

# クエリのクラス
class query_class:
    # 変数初期化
    def __init__(self):
        self.min = 0
        self.max = 0
        self.mu = 0
        self.sigma = 0
        self.mode = 0
        self.lambd = 0.0
        self.alpha = 0.0
        self.beta = 0.0
        self.trials = 1
        self.type = ""
        self.err = {}

    # クエリパラメータの取得
    def get(self, distribution):
        try:
            # type: 整数 or 浮動小数点数
            arg_type = request.args.get("type")
            if self.type is not None:
                self.type = arg_type

            # trials: 試行回数（発生させる乱数の数）
            arg_trials = request.args.get("trials")
            if arg_trials is not None:
                self.trials = int(arg_trials)

            # 指定された確率分布関数が...
            # 一様分布 or 三角分布の場合  
            if distribution == "uniform" or distribution == "triangular":
                req_min = request.args.get("min")
                req_max = request.args.get("max")

                if self.type == "int":
                    if req_min is None:
                        self.min = -sys.maxsize
                    else:
                        self.min = float(req_min)
                    
                    if req_max is None:
                        self.max = sys.maxsize
                    else:
                        self.max = float(req_max)
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
                        self.mode = float(req_mode)
                        
                return

            # 正規分布の場合
            elif distribution == "normal":
                req_mu = request.args.get("mu")
                req_sigma = request.args.get("sigma")

                if req_mu is None:
                    self.mu = 0
                else:
                    self.mu = float(req_mu)
                
                if req_sigma is None:
                    self.sigma = 1
                else:
                    self.sigma = float(req_sigma)
                return

            # ラムダ分布の場合
            elif distribution == "lambda":
                req_lambd = request.args.get("lambd")

                if req_lambd is None:
                    self.lambd = 1
                else:
                    self.lambd = 1/float(req_lambd)
                return

            # ベータ分布 or ガンマ分布の場合
            elif distribution == "beta" or distribution == "gamma":
                req_alpha = request.args.get("alpha")
                req_beta = request.args.get("beta")

                if req_alpha is None:
                    self.alpha = 1.0
                else:
                    self.alpha = float(req_alpha)
                
                if req_beta is None:
                    self.beta = 2.0
                else:
                    self.beta = float(req_beta)
                return

        except ValueError:
            self.err["error_num"] = 1
            self.err["error_message"] = "Error: Arguments are incorrect"
            return


# ルートディレクトリ：接続確認用
@app.route('/')
def root_index():
    return "Successfully accessed."

# uniform: 一様分布
@app.route('/random/uniform', methods=["GET"])
def uniform_index():
    rand = []
    jrand = {}
    # クエリパラメータの取得
    query = query_class()
    query.get("uniform")

    # クエリ取得中にエラーが発生したらエラーをresponseとして返す
    if 'error_num' in query.err:
        return json.dumps(query.err)
    
    try:
        # trials回, 乱数を生成
        for i in range(query.trials):
            if query.type == "int":
                rand.append(random.randint(query.min, query.max))
            else:
                rand.append(random.uniform(query.min, query.max))
    except ValueError:
        # パラメータが間違っていることによりエラーが発生した場合はエラーを返す
        jrand["error_num"] = 2
        jrand["error_message"] = "Error: Wrong parameter"
        return json.dumps(jrand)

    # JSON形式に変換して完了
    jrand["rand_array"] = rand
    return json.dumps(jrand)

# normal: 正規分布
@app.route('/random/normal', methods=["GET"])
def normal_index():
    rand = []
    jrand = {}
    # クエリパラメータの取得
    query = query_class()
    query.get("normal")

    # クエリ取得中にエラーが発生したらエラーをresponseとして返す
    if 'error_num' in query.err:
        return json.dumps(query.err)

    try:
        # trials回, 乱数を生成
        for i in range(query.trials):
            rand_temp = random.gauss(query.mu, query.sigma)
            if query.type == "int":
                rand_temp = int(rand_temp)
            rand.append(rand_temp)
    except ValueError:
        # パラメータが間違っていることによりエラーが発生した場合はエラーを返す
        jrand["error_num"] = 2
        jrand["error_message"] = "Error: Wrong parameter"
        return json.dumps(jrand)

    # JSON形式に変換して完了
    jrand["rand_array"] = rand
    return json.dumps(jrand)

# beta: ベータ分布
@app.route('/random/beta', methods=["GET"])
def beta_index():
    rand = []
    jrand = {}
    # クエリパラメータの取得
    query = query_class()
    query.get("beta")

    # クエリ取得中にエラーが発生したらエラーをresponseとして返す
    if 'error_num' in query.err:
        return json.dumps(query.err)

    try:
        # trials回, 乱数を生成
        for i in range(query.trials):
            rand_temp = random.betavariate(query.alpha, query.beta)
            if query.type == "int":
                rand_temp = int(rand_temp)
            rand.append(rand_temp)
    except ValueError:
        # パラメータが間違っていることによりエラーが発生した場合はエラーを返す
        jrand["error_num"] = 2
        jrand["error_message"] = "Error: Wrong parameter"
        return json.dumps(jrand)

    # JSON形式に変換して完了
    jrand["rand_array"] = rand
    return json.dumps(jrand)

# triangular: 三角分布
@app.route('/random/triangular', methods=["GET"])
def triangular_index():
    rand = []
    jrand = {}
    # クエリパラメータの取得
    query = query_class()
    query.get("triangular")

    # クエリ取得中にエラーが発生したらエラーをresponseとして返す
    if 'error_num' in query.err:
        return json.dumps(query.err)

    try:
        # trials回, 乱数を生成
        for i in range(query.trials):
            rand_temp = random.triangular(query.min, query.max, query.mode)
            if query.type == "int":
                rand_temp = int(rand_temp)
            rand.append(rand_temp)
    except ValueError:
        # パラメータが間違っていることによりエラーが発生した場合はエラーを返す
        jrand["error_num"] = 2
        jrand["error_message"] = "Error: Wrong parameter"
        return json.dumps(jrand)

    # JSON形式に変換して完了
    jrand["rand_array"] = rand
    return json.dumps(jrand)

# lambda: ラムダ分布
@app.route('/random/lambda', methods=["GET"])
def lambda_index():
    rand = []
    jrand = {}
    # クエリパラメータの取得
    query = query_class()
    query.get("lambda")

    # クエリ取得中にエラーが発生したらエラーをresponseとして返す
    if 'error_num' in query.err:
        return json.dumps(query.err)

    try:
        # trials回, 乱数を生成
        for i in range(query.trials):
            rand_temp = random.expovariate(query.lambd)
            if query.type == "int":
                rand_temp = int(rand_temp)
            rand.append(rand_temp)
    except ValueError:
        # パラメータが間違っていることによりエラーが発生した場合はエラーを返す
        jrand["error_num"] = 2
        jrand["error_message"] = "Error: Wrong parameter"
        return json.dumps(jrand)

    # JSON形式に変換して完了
    jrand["rand_array"] = rand
    return json.dumps(jrand)

# gamma: ガンマ分布
@app.route('/random/gamma', methods=["GET"])
def gamma_index():
    rand = []
    jrand = {}
    # クエリパラメータの取得
    query = query_class()
    query.get("gamma")

    # クエリ取得中にエラーが発生したらエラーをresponseとして返す
    if 'error_num' in query.err:
        return json.dumps(query.err)

    try:
        # trials回, 乱数を生成
        for i in range(query.trials):
            rand_temp = random.gammavariate(query.alpha, query.beta)
            if query.type == "int":
                rand_temp = int(rand_temp)
            rand.append(rand_temp)
    except ValueError:
        # パラメータが間違っていることによりエラーが発生した場合はエラーを返す
        jrand["error_num"] = 2
        jrand["error_message"] = "Error: Wrong parameter"
        return json.dumps(jrand)

    # JSON形式に変換して完了
    jrand["rand_array"] = rand
    return json.dumps(jrand)

if __name__ == '__main__':
    app.run()
