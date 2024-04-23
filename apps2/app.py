from flask import Flask, render_template, request, redirect, send_from_directory, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from apps import models
from apps import forms
from .models import User, Symptom
from .extensions import db
import datetime
import os
from werkzeug.utils import secure_filename

# flaskのインスタンスを作成
app = Flask(__name__)
#設定ファイルの読み込み
app.config.from_pyfile('settings.py')
#SQLAlchemyのインスタンスを作成
db = SQLAlchemy(app)
#Migrateオブジェクトを作成し、FlaskオブジェクトとSQLAlchemyオブジェクトを登録
migrate = Migrate(app, db)

# ルーティングの設定（トップページ）
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# ルーティングの設定（同意文書）
@app.route('/notice', methods=['GET', 'POST'])
def notice():
    return render_template('notice.html')

# ルーティングの設定（年齢、性別、発症時期、自覚症状など）
@app.route('/symptom', methods=['GET', 'POST'])
def symptom():
    if request.method == 'POST':
        user = Symptom(
            id=request.form.get('id'),
            sex=request.form.get('sex'),
            birth_year=int(request.form.get('birth_year')),
            birth_month=int(request.form.get('birth_month')),
            birth_day=int(request.form.get('birth_day')),
            onset_year=int(request.form.get('onset_year')),
            onset_month=int(request.form.get('onset_month')),
            onset_day=int(request.form.get('onset_day')),
            morning_stiffness=request.form.get('morning_stiffness'),
            stiffness_duration=int(request.form.get('stiffness_duration')),
            pain_level=int(request.form.get('pain_level'))       
            )
        
        db.session.add(user)
        db.session.commit()

        # 年齢の計算
        today = datetime.date.today()
        age = user.calculate_age(today.year, today.month, today.day)

        # ここでageを使う処理を追加できます

    years = range(1920, 2021)
    months = range(1, 13)
    days = range(1, 32)
    stiffness_durations = [0, 5, 10, 15, 20, 30, 40, 50, 60, 120]

    return render_template('symptom.html', years=years, months=months, days=days, stiffness_durations=stiffness_durations)

# ルーティングの設定（症状のある関節の特定）
@app.route('/joints_fig', methods=['GET', 'POST'])
def joints_fig():
    if request.method == 'POST':
        # フォームからチェックされた関節を抽出
        checked_joints = request.form.getlist('joint')
        
        # distalとproximalカテゴリーに対応する関節を定義
        distal_joints_list = ['pip_joint_left', 'thumb_ip_joint_left', 'mp_joint_hand_left', 'wrist_joint_left', 'mp_joint_foot_left']
        proximal_joints_list = ['elbow_joint_left', 'shoulder_joint_left', 'hip_joint_left', 'knee_joint_left', 'ankle_joint_left']

        # 各カテゴリーでチェックされた関節の数をカウント
        distal_joints = sum(joint in checked_joints for joint in distal_joints_list)
        proximal_joints = sum(joint in checked_joints for joint in proximal_joints_list)

        # 必要に応じてカウントの処理を行い、例えばクライアントに返す
        return f'distal joints: {distal_joints}, proximal joints: {proximal_joints}'
    else:
        return render_template('joints_fig.html')

# ルーティングの設定（臨床検査結果）
@app.route('/labo_exam', methods=['GET', 'POST'])
def labo_exam():
    if request.method == 'POST':
        # フォームから数値を取得
        rf = request.form.get('rf', type=float)
        acpa = request.form.get('acpa', type=float) 
        crp = request.form.get('crp', type=float)
        esr = request.form.get('esr', type=float)
    else:#GETリウエストの場合
        return render_template('labo_exam.html')   
    
UPLOAD_FOLDER = '/path/to/upload/folder'  # Replace '/path/to/upload/folder' with the actual path to your upload folder

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'heic', 'heif', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


#このスクリプトが直接実行された場合にのみアプリケーションが起動するようにする    
if __name__ == '__main__':
    app.run(debug=True)



