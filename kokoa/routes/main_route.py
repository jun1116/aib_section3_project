from flask import Blueprint, render_template, request, flash, session, g, url_for
# from twit_app.utils import main_funcs
from kokoa.models.user_model import User, Company, Room
# from kokoa.forms import UserCreateForm
# from services.embedding_api import compare

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from kokoa import db

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

# @bp.route('/logedin/')
# def logedin():

#     return render_template('friends.html',user=user, g=g)

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
# @bp.route('/friends/')
# def 

# @bp.route('/compare', methods=["GET", "POST"])
# def compare_index():
#     """
#     users 에 유저들을 담아 넘겨주세요. 각 유저 항목은 다음과 같은 딕셔너리
#     형태로 넘겨주셔야 합니다.
#      -  {
#             "id" : "유저의 아이디 값이 담긴 숫자",
#             "username" : "유저의 유저이름 (username) 이 담긴 문자열"
#         }

#     prediction 은 다음과 같은 딕셔너리 형태로 넘겨주셔야 합니다:
#      -   {
#              "result" : "예측 결과를 담은 문자열입니다",
#              "compare_text" : "사용자가 넘겨준 비교 문장을 담은 문자열입니다"
#          }
#     """
#     user_list = user_model.User.query

#     users = user_model.User.query
#     prediction = {'result':' ','compare_text':' '}##
#     if request.method == "POST":
#         # print(request.form)
#         user_1_id = request.form['user_1']
#         user_2_id = request.form['user_2']
#         text = request.form['compare_text']
#         # POST 일 경우에 필요한 코드를 작성해 주세요
#         # print(request.form)
        
#         user1 = user_model.User.query.get(user_1_id)
#         user2 = user_model.User.query.get(user_2_id)
#         # print(user1.tweet, user2)
#         pred = main_funcs.predict_text([user1,user2], text)
#         # print(pred)
#         prediction['result'] = pred
#         prediction['compare_text'] = text
        
#     return render_template('compare_user.html', users=users, prediction=prediction)


# @bp.route('/user')
# def user_index():
#     """
#     user_list 에 유저들을 담아 템플렛 파일에 넘겨주세요
#     """

#     msg_code = request.args.get('msg_code', None)
    
#     alert_msg = main_funcs.msg_processor(msg_code) if msg_code is not None else None
    
#     user_list = user_model.User.query

#     return render_template('user.html', alert_msg=alert_msg, user_list=user_list)
