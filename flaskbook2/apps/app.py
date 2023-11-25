from flask import Flask
from pathlib import Path
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
#データベース(sqlalchemy)のインスタンス化
db = SQLAlchemy()
csrf = CSRFProtect()


#create_app関数の作成
def create_app():
    app = Flask(__name__)
    from crud import views as crud_views
    app.register_blueprint(crud_views.crud, url_prefix="/crud")
    app.debug = True
    app.config.from_mapping(
        SECRET_KEY="2gfyurhu32mn",
        SQLALCHEMY_DATABASE_URI=
        f"sqlite:///{Path(__file__).parent.parent/'local.sqlite'}",
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        WTF_CSRF_SECRET_KEY = "dsy4ajige3hui34",
        SQLALCHEMY_ECHO = True
    )
    csrf.init_app(app)
    db.init_app(app)
    Migrate(app,db)
    return app
