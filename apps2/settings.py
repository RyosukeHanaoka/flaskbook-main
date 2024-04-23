import os

#モジュールの親ディレクトリのフルパスを取得
basedir = os.path.dirname(os.path.dirname(__file__))
#親ディレクトリをデータベースに設定
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
#シークレットキーの値として10バイトの文字列をランダムに生成
SECRET_KEY = os.urandom(10)

# 管理者のユーザー名とパスワードを設定
USERNAME = 'admin'
PASSWORD = '91235499'