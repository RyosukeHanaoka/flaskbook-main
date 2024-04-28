from apps.app import db
from crud.forms import UserForm
from crud.models import User
from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required

# Blueprintでcrudアプリを生成する
crud = Blueprint(
    # Blueprintの名前を"crud"に指定する
    "crud",
    # ファイルの名前を指定する
    __name__,
    # テンプレートフォルダを指定する
    template_folder="templates",
    # 静的フォルダを指定する
    static_folder="static",
)
# indexエンドポイントを作成しindex.htmlを返す
@crud.route("/")
# ログインが必要なエンドポイントにする
@login_required
# index関数を作成する
def index():
    # index.htmlを返す
    return render_template("crud/index.html")

# sqlエンドポイントを作成し、SQLを実行する
@crud.route("/sql")
# ログインが必要なエンドポイントにする
@login_required
# sql関数を作成する
def sql():
    # Userテーブルの全てのデータを取得する
    db.session.query(User).all()
    # コンソールログを確認する
    return "コンソールログを確認してください"

# users/newエンドポイントを作成し、新規ユーザーを作成する
@crud.route("/users/new", methods=["GET", "POST"])
@login_required
# create_user関数を作成する
def create_user():
    # UserFormをインスタンス化する
    form = UserForm()

    # フォームの値をバリデートする
    if form.validate_on_submit():
        # ユーザーを作成する
        user = User(
            # フォームの値を取得する
            username=form.username.data,
            # フォームの値を取得する
            email=form.email.data,
            # フォームの値を取得する
            password=form.password.data,
        )

        # ユーザーを追加してコミットする
        db.session.add(user)
        # コミットする
        db.session.commit()

        # ユーザーの一覧画面へリダイレクトする
        return redirect(url_for("crud.users"))
    # フォームの値がバリデートされなかった場合はcreate.htmlを返す
    return render_template("crud/create.html", form=form)

# usersエンドポイントを作成し、ユーザーの一覧を取得する
@crud.route("/users")
# ログインが必要なエンドポイントにする
@login_required
# users関数を作成する
def users():
    """ユーザーの一覧を取得する"""
    users = User.query.all()
    # ユーザーの一覧をテンプレートに渡す
    return render_template("crud/index.html", users=users)


# methodsにGETとPOSTを指定する
@crud.route("/users/<user_id>", methods=["GET", "POST"])
# ログインが必要なエンドポイントにする
@login_required
# edit_user関数を作成する
def edit_user(user_id):
    # UserFormをインスタンス化する
    form = UserForm()

    # Userモデルを利用してユーザーを取得する
    user = User.query.filter_by(id=user_id).first()

    # formからサブミットされた場合はユーザーを更新しユーザーの一覧画面へリダイレクトする
    if form.validate_on_submit():
        # フォームの値を取得しユーザーを更新する
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        # ユーザーをコミットする
        db.session.add(user)
        # コミットする
        db.session.commit()
        # ユーザーの一覧画面へリダイレクトする
        return redirect(url_for("crud.users"))

    # GETの場合はHTMLを返す
    return render_template("crud/edit.html", user=user, form=form)

# users/<user_id>/deleteエンドポイントを作成し、ユーザーを削除する
@crud.route("/users/<user_id>/delete", methods=["POST"])
@login_required
# delete_user関数を作成する
def delete_user(user_id):
    # ユーザーを取得する
    user = User.query.filter_by(id=user_id).first()
    # ユーザーを削除する
    db.session.delete(user)
    # コミットする
    db.session.commit()
    # ユーザーの一覧画面へリダイレクトする
    return redirect(url_for("crud.users"))





