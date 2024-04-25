from datetime import datetime
from .extensions import db
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

class User(db.Model):
    __tablename__="user"
    #自動的に連番を生成するidカラムを追加
    id = db.Column(db.Integer, #データ型は整数
                primary_key=True,#主キーに設定
                autoincrement=True)#自動的に増分する
    #ユーザー名（メールアドレス）を含める。
    email = db.Column(
        db.String(120),#データ型は文字列
        unique=True,#一意制約を設定
        nullable=False)#登録を必須に設定
    #ハッシュ化されたパスワードを含める
    password_hash = db.Column(db.String(128))#データ型は文字列
    #パスワードをハッシュ化するメソッド
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    #パスワードをチェックするメソッド
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    #ユーザー名を返すメソッド
    def __repr__(self):
        return '<User {}>'.format(self.email)
    #登録日時を追加
    created_at = db.Column(db.DateTime, default=datetime.now)
    #更新日時を追加
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class Symptom(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    sex = db.Column(db.String(10))
    birth_year = db.Column(db.Integer)
    birth_month = db.Column(db.Integer)
    birth_day = db.Column(db.Integer)
    onset_year = db.Column(db.Integer)
    onset_month = db.Column(db.Integer)
    onset_day = db.Column(db.Integer)
    morning_stiffness = db.Column(db.String(50))
    stiffness_duration = db.Column(db.Integer)
    pain_level = db.Column(db.Integer)

    def calculate_age(self, current_year, current_month, current_day):
        age = current_year - self.birth_year
        if (current_month, current_day) < (self.birth_month, self.birth_day):
            age -= 1
        return age
    
def joint_score(proximal_joints, distal_joints):
    joint_score = 0  # 関節スコアの初期値を設定
    # "distal_joints"が0のときの条件
    if "distal_joints" == 0:
        if proximal_joints == 0:
            return 0
        else:
            return 1
    # distal_jointsが0より大きい数のときの条件
    else:
        # proximal_joints + distal_jointsの合計が11以上の場合
        if proximal_joints + distal_joints >= 11:
            return 5
        # proximal_joints + distal_jointsの合計が10未満の場合
        elif proximal_joints + distal_joints < 10:
        # distal_jointsが3以下の場合
            if distal_joints <= 3:
                return 2
        # distal_jointsが4以上の場合
            else:
                return 3


def immunology_score(rf, acpa):
    immunology_score = 0  # 免疫学的スコアの初期値を設定
    # 最初の条件群
    if rf >= 45:
        return 2
    elif acpa >= 13.5:
        return 2
    elif rf >= 15:
        return 1
    elif acpa >= 4.5:
        return 1
    else:
        return 0

def inflammation_score(crp, esr, sex):
    # crpとesrの値によってスコアを返す
    if crp > 0.3:
        return 1
    elif sex == 0:
        if esr > 10:
            return 1
        else:
            return 0
    elif sex == 1:
        if esr > 15:
            return 1
        return 0