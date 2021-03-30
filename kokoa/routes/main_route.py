from flask import Blueprint, render_template, request, flash, session, g, url_for
# from twit_app.utils import main_funcs
from kokoa.models.user_model import User, Company, Room, SubwayPassenger
# from kokoa.forms import UserCreateForm
# from services.embedding_api import compare

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from kokoa import db
import pandas as pd
# from urllib.request import urlretrieve
import pickle


bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    # return 'hello'
    # form = UserCreateForm()
    return render_template('index.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None: g.user=None
    else: g.user = User.query.get(user_id)

@bp.route('/signup/', methods=['GET','POST'])
def signup():
    print('signup input : ',request.form)
    username=request.form['username']
    password=request.form['password']
    # form = UserCreateForm()
    if request.method=='POST':
        user = User.query.filter_by(username=username ).first()
        if not user: #유저가 존재하지 않음 -> 생성
            user = User(username=username,\
                password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return f'<script> alert("유저 생성 완료. ID : {username}, PASSWORD : {password}"); location.href="/" </script>'
            # return redirect(url_for('main.index'))
        else: #유저가 이미 존재함 -> 뒤로가기
            return f'<script> alert("이미 존재하는 user입니다. 다른 이름을 입력하세요"); location.href="/" </script>'
            # flash('이미 존재하는 사용자입니다')
            # return '이미 존재하는 username입니다.'
    return f'<script> alert("오류. 다시 시작하세요"); location.href="/" </script>'

@bp.route('/login', methods=['GET','POST'])#로그인화면에서입장
@bp.route('/friends/', methods=['GET','POST'])#이후 화면에서 friends로 돌아옴
def login():
    print("login input : ",request.form)
    companys = Company.query.all()
    print(session)
    if session.get('user_id'):# 이미 로그인 된 경우
        user = User.query.get(session['user_id'])
        return render_template('friends_ex.html',user=user, g=g, companys=companys)

    username=request.form['username']
    password=request.form['password']
    user = User.query.filter_by(username=username ).first()
    if not user: #입력된 이름의 유저 db에 없는경우
        return f'<script> alert("존재하지 않는 유저입니다. Username을 확인하거나, 회원가입을 진행하세요"); location.href="/" </script>'
    else: #존재하는 유저에 대한 입력
        input_pwd = generate_password_hash(password)
        if check_password_hash(user.password, password):
            # session['key']
            session.clear()
            session['user_id'] = user.id
            print(session, g)
            return render_template('friends_ex.html',user=user, g=g, companys=companys)
        else:
            # 'password 가 틀렸습니다.'
            return f'<script> alert("비밀번호가 틀렸습니다."); location.href="/" </script>'
            # flash('이미 존재하는 사용자입니다')
    return 'end'

@bp.route('/logout/')
def logout():
    session.clear()
    print(session)
    return redirect(url_for('main.index'))

@bp.route('/usersetting')
def usersetting():
    print('USER SETTING PAGE')
    return render_template('settings.html')

@bp.route('/userdelete')
def userdelete():
    print("User Delete Page")
    user_id = session['user_id']
    # print(user_id)
    user = User.query.get(user_id)
    rooms = Room.query.filter(Room.user_id==user_id).all()
    # print(rooms)
    db.session.delete(user)
    for room in rooms:
        db.session.delete(room)
    db.session.commit()
    return logout()

@bp.route('/updateSubway')#월별 시간별 지하철 승하차인원 데이터 (2019,2020 평균) 로드
def updateSubway():
    sub = pd.read_csv('https://blog.kakaocdn.net/dn/cmDivW/btq1lb1aH3p/xnB8ylQePEudFkuz4x9iak/subway_date.csv?attach=1&knm=tfile.csv').to_dict(orient='records')
    for i in sub:
        db.session.add(SubwayPassenger(month=i['month'],hour=i['hour'],holiday=i['휴일'],insub=int(float(i['승차'])), outsub= int(float(i['하차']))) )
    db.session.commit()
    return redirect(url_for('chat.chats'))

@bp.route('/updateModel')
def updateModel():
    # model = 
    urlretrieve('https://blog.kakaocdn.net/dn/M976c/btq1laBtmQ3/XxmZ0qEixddI2DMrLHg890/lgb.pkl?attach=1&knm=tfile.pkl', "./lgb.pkl")
    lgb= joblib.load('./lgb.pkl')  
    # pickle.load(open('./lgb.pkl','rb'))
    return redirect(url_for('chat.chats'))


