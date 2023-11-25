from flask import Flask, render_template,url_for, request, session
from flask.views import MethodView
import random

#インスタンスの生成
app = Flask(__name__)

#javaでいうところのアノテーション
@app.route("/<id>/<password>")
def hellow_world(id, password):
    flg = None
    list = ["こんにちは","こんばんは", 24, "aaaaa", True]
    msg = "id: %s, password:%s" % (id, password)
    return render_template("./index.html", title = "jinja", message = msg, data = list)

@app.route("/", methods = {"GET"})
def index():
    msg = "初期の画面"
    list = [10, 20, 30, 40, 22]
    return render_template("index.html",message = msg ,data = list)

#POSTで受け取ったパラメータの受け取り
@app.route("/", methods = ["POST"])
def form():
    field = request.form.get("check")
    radio = request.form.get("radio")
    sel = request.form.getlist("sel")
    return render_template("index.html", title = "Form Sample", message = [field, radio, sel])

#テンプレートフィルター
@app.template_filter("sum")
def sum_filter(data):
    total = 0
    for i in data:
        total += i
    return total
app.jinja_env.filters["sum"] = sum_filter

#メソッドビューの定義
app.secret_key = b"123456789"
class HelloAPI(MethodView):
    send = ""
    def get(self):
        #session["bb"] = []
        return render_template("next.html", title = "Next Page", message = "何か書いてください．", send = HelloAPI.send,  data = list)
    def post(self):
        list = session["bb"]
        list.append(random.randrange(5,100))
        session["bb"] = list
        smp = []
        if len(list) == 10:
            list = session.pop("bb", [])
            session["bb"] = ["test"]
        HelloAPI.send = request.form.get("send")
        return render_template("next.html", title = "Next Page", message = "書いてみました．", send = HelloAPI.send, data = list, test = smp) 
app.add_url_rule("/hello/", view_func=HelloAPI.as_view("hello"))  
if __name__ == "__main__":
    app.debug = True
    app.run(host = "localhost")