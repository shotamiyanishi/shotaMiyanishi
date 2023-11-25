from flask import Flask, render_template, url_for, redirect, request, flash, session
from email_validator import validate_email, EmailNotValidError
import logging
from flask_debugtoolbar import DebugToolbarExtension
import os
from flask_mail import Mail, Message


app = Flask(__name__)
#秘密鍵の追加(flash, sessionに使用)
app.config["SECRET_KEY"] = "12gayde8yge4sy"
app.logger.setLevel(logging.DEBUG)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.debug = True
toolbar = DebugToolbarExtension(app)
#メールのコンフィグ
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME") 
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")
mail = Mail(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hello/<name>", endpoint = "hello-endpoint")
def hello(name):
    return "hello World" + name

@app.route("/contact")
def contact():
    session["hoge"] = "hoge宮西翔太"
    return render_template("contact.html")

@app.route("/contact/complete", methods = ["GET" ,"POST"])
def contact_complete():
    if request.method == "POST":
        user_name = request.form["user_name"]
        email = request.form["email"]
        contents = request.form["contents"]
        is_valid = True
        if not user_name:
            flash("ユーザ名は必須です．")
            is_valid = False
        if not email:
            flash("メールアドレスは必須です．")
            is_valid = False
            
        try:
            validate_email(email)
        except EmailNotValidError:
            flash("メールアドレスの形式で入力してください．")
            is_valid = False
        if not contents:
            flash("お問い合わせ内容は必須です．")
            is_valid = False
        
        if not is_valid:
            return redirect(url_for("contact"))
        flash("お問い合わせありがとうございました．")
        #リダイレクト
        send_email("seba47zt@gmail.com", "お問い合わせありがとうございました．", "contact_email")
        return redirect(url_for("contact_complete"))
    hogeso = session["hoge"]
    return render_template("contact_complete.html", hoge = hogeso)

with app.test_request_context():
    print(url_for("hello-endpoint", name = "World"))
    print(url_for("index"))
    print(url_for("contact"))
    
def send_email(to, subject, template):
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + ".txt")
    msg.html = render_template(template + ".html")
    mail.send(msg)