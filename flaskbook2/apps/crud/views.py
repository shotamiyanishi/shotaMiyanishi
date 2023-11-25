from flask import Blueprint, render_template, redirect, url_for
from app import db
from crud.models import User
from crud.forms import UserForm
crud = Blueprint(
    "crud",
    __name__,
    template_folder="templates",
    static_folder="statics"
)

#indexエンドポイントの作成
@crud.route("/")
def index():
    return render_template("crud/index.html")

#全件取得
@crud.route("/sql")
def sql():
    User.query.all()
    return "コンソールを確認してください．"

#ユーザーの新規作成
@crud.route("/users/new", methods = ["GET", "POST"])
def create_user():
    form = UserForm()
    #フォームをバリデートする
    if form.validate_on_submit():
        #ユーザを作成する
        user = User (
        username = form.username.data,
        email = form.email.data,
        password = form.password.data
        )
        #ユーザを実際に追加する．
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("crud.users"))
    return render_template("crud/create.html", form = form)

#ユーザー一覧を表示する
@crud.route("/users", methods = ["GET", "POST"])
def users():
    """userの一覧を取得する"""
    users = User.query.all()
    return render_template("crud/index.html", users = users)

#ユーザーの情報を変更する
@crud.route("/users/<user_id>", methods = ["GET", "POST"])
def edit_user(user_id):
    form = UserForm()
        
    #Userモデルを利用してデータを取ってくる．
    user = User.query.filter_by(id = user_id).first()
    count = User.query.filter_by(id = user_id).count()
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("crud.users"))
    return render_template("crud/edit.html", user = user, form = form, size = count)

#ユーザを削除する
@crud.route("users/<user_id>/delete")
def delete_user(user_id):
    user = User.query.filter_by(id = user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("crud.users"))
    
        
        
    