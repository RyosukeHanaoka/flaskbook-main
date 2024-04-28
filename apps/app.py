import sys
print(sys.path)
#Flaskフレームワークとテンプレートをレンダリングするための関数をインポートする。
from flask import Flask, render_template
#Flaskアプリでユーザーのログインを管理するためのLoginManagerをインポートする。
from flask_login import LoginManager
#Flask-Migrateをインポートし、データベースのマイグレーションを可能にする
from flask_migrate import Migrate
#SQLAlchemyというORM（オブジェクトリレーショナルマッピング）をインポートする
from flask_sqlalchemy import SQLAlchemy
#Flask-WTFのCSRF保護機能をインポートする
from flask_wtf.csrf import CSRFProtect
#アプリケーションの設定を読み込むためのconfigをインポートする
from pathlib import Path
from apps import config
#SQLAlchemyのインスタンスを作成する
db = SQLAlchemy()
#CSRF保護のためのインスタンスを作成する
csrf = CSRFProtect()
# ログイン管理のためのインスタンスを作成
login_manager = LoginManager()
# ログインしていないユーザーをリダイレクトするエンドポイントを設定
login_manager.login_view = "auth.signup"
# login_message属性にログイン後に表示するメッセージを指定する
# ここでは何も表示しないよう空を指定する
login_manager.login_message = ""


# アプリケーションを作成する関数"create_app"を作成する
def create_app():
    # Flaskインスタンス生成
    app = Flask(__name__)
    config_key=os.getenv('CONFIG_KEY', 'local')
    #指定された設定キーに基づいて構成を読み込む
    app.config.from_object(config[config_key])
    """app.config.from_mapping(
        SECRET_KEY="2AZSMss3p5QPbcY2hBsJ",
        SQLALCHEMY_DATABASE_URI=
        f"sqlite:///{Path(__file__).parent.parent/'local.sqlite'}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True,
        WTF_CSRF_SECRET_KEY="AuwzyszU5sugKN7KZs6f"
    )   """
    # SQLAlchemyとアプリを連携するために初期化する
    db.init_app(app)
    # Migrateとアプリを連携する
    Migrate(app, db)
    # CSRF保護をアプリに適用する
    csrf.init_app(app)
    # login_managerをアプリケーションと連携する
    login_manager.init_app(app)

    # crudパッケージからCRUD操作のためのviewsをimportする
    from apps.crud import views as crud_views

    # register_blueprintを使い、CRUDのビューをアプリに登録
    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    # これから作成するauthパッケージから認証のviewsをimportする
    from apps.auth import views as auth_views

    # register_blueprintを使いviewsのauthをアプリへ登録する
    app.register_blueprint(auth_views.auth, url_prefix="/auth")

    # これから作成するdetectorパッケージからviewsをimportする
    from apps.detector import views as dt_views

    # register_blueprintを使いviewsのdtをアプリへ登録する
    app.register_blueprint(dt_views.dt)

    # これから作成するmy_appsパッケージからviewsをimportする
    from apps.crud_data import views as my_views

    # register_blueprintを使いviewsのdataをアプリへ登録する
    app.register_blueprint(my_views.data)

    # カスタムエラー画面を登録する
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)

    return app


# 登録したエンドポイント名の関数を作成し、404や500が発生した際に指定したHTMLを返す
def page_not_found(e):
    """404 Not Found"""
    return render_template("404.html"), 404


def internal_server_error(e):
    """500 Internal Server Error"""
    return render_template("500.html"), 500




