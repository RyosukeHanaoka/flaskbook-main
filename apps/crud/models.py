from datetime import datetime
# apps.appからdbとlogin_managerをimportする
from apps.app import db, login_manager
# flask_loginからUserMixinをimportする
# UserMixinは、ユーザー情報を取得するためのクラス
from flask_login import UserMixin
# werkzeug.securityからcheck_password_hashとgenerate_password_hashをimportする
# check_password_hashは、パスワードをチェックするための関数
# generate_password_hashは、パスワードをハッシュ化するための関数
#werkzeug.securityは、セキュリティ関連の機能を提供するモジュール
from werkzeug.security import check_password_hash, generate_password_hash


# db.Modelを継承したUserクラスを作成する
class User(db.Model, UserMixin):
    # テーブル名を指定する
    __tablename__ = "users"
    # カラムを定義する
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True)
    email = db.Column(db.String, unique=True, index=True)
    password_hash = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # backrefを利用しrelation情報を設定する
    user_images = db.relationship("UserImage", backref="user")

    # パスワードをセットするためのプロパティ
    @property
    # パスワードを取得するためのゲッター関数でエラーを返す
    def password(self):
        # AttributeErrorを返す
        raise AttributeError("読み取り不可")

    # パスワードをセットするためのセッター関数でハッシュ化したパスワードをセットする
    # setterとは、プロパティの値を設定するためのメソッド
    # setterのimportは、from flask_sqlalchemy import SQLAlchemyで行う
    @password.setter
    # パスワードをセットするためのセッター関数でハッシュ化したパスワードをセットする
    def password(self, password):
        # generate_password_hash関数を使ってパスワードをハッシュ化する
        self.password_hash = generate_password_hash(password)

    # パスワードチェックをする
    def verify_password(self, password):
        # check_password_hash関数を使ってパスワードをチェックする
        return check_password_hash(self.password_hash, password)

    # メールアドレス重複チェックをする
    def is_duplicate_email(self):
        # User.query.filter_by(email=self.email).first()がNoneでない場合に重複していると判定する
        return User.query.filter_by(email=self.email).first() is not None


# ログインしているユーザー情報を取得する関数を作成する
@login_manager.user_loader
# ユーザーIDを引数に取り、ユーザー情報を取得する
def load_user(user_id):
    # User.query.get(user_id)でユーザー情報を取得する
    return User.query.get(user_id)




