from flask import Blueprint, render_template, request, session, url_for
from kokoa.models.user_model import User, Company, Room, Chat
from kokoa import db
from func.company_answer import company_answer,gangnamBike

bp = Blueprint('chat',__name__)

@bp.route('/chats/')#채팅방리스트 페이지(chats)
def chats():
    user_id = session['user_id']
    user = User.query.get(user_id)
    rooms = Room.query.filter(Room.user_id==user_id).all()
    print('userid : ',user_id,'\tUSER : ', user)
    print('ROOMS : ',rooms)
    session['room_id'] = None
    roomList = []
    for room in rooms:
        roomList.append(
            {'company_name':Company.query.get(room.company_id).companyname
            ,'room_id':room.id
            ,'last_chat': Chat.query.filter(Chat.room_id==room.id).order_by(Chat.time.desc()).first() 
            })
    return render_template('chats.html', roomlist=roomList, )

@bp.route('/chatdetail/<int:room_id>')#주고받은 메시지 띄울 페이지
def chatdetail(room_id):
    room = Room.query.get(room_id)
    chats = Chat.query.filter(Chat.room_id==room_id).order_by(Chat.time).all()
    company = Company.query.get(room.company_id)
    # print(chats)
    session['room_id']=room.id
    return render_template('chatdetail.html',companyname=company.companyname ,room=room,chats=chats)

@bp.route('/chatdetail/', methods=['POST'])
def reply():
    form = request.form
    text = form['reply']
    if text:
        print('세션에 남은 유저아이디',session['user_id'])
        print('세션에 남은 룸아이디',session['room_id'])
        # print(data)
        db.session.add(Chat(room_id=session['room_id'], text=text, isuser=1))

        # TODO : 회사의 답변을 등록해야함
        db_room = Room.query.get(session['room_id'])
        company = Company.query.filter(Company.id==db_room.id).first()
        answer = company_answer(company.id, text)
        # company_answer = gangnamBike(text)
        if answer:
            db.session.add(Chat(room_id=session['room_id'], text=answer, isuser=0))
            db.session.commit()
    return chatdetail(session['room_id'])

@bp.route('/deletechat')
def deletechat():
    # print(request.form)
    # print(session['room_id'])
    room = Room.query.get(session['room_id'])
    db.session.delete(room)
    db.session.commit()
    session['room_id']=None
    return chats()

@bp.route('/chatstart', methods=['GET']) #Friends화면의 회사를 눌러서 채팅 시작 -> 채팅이 이미 있는경우 해당 방 입장, 없는경우 방생성 & 환영인사생성
def chatstart():
    # get_company = request.args['company']
    # company_id = int(get_company.split()[3][0])
    # company_id = 
    print('user : ', session['user_id'])
    # print(request.args)
    company_id = int(request.args['company'])
    #1. 채팅방 찾기
    room = Room.query.filter(Room.user_id==session['user_id'], Room.company_id==company_id).first()
    print('Finded Room : ',room)
    
    #이미 채팅방이 있다 -> 해당채팅방으로
    if room:
        return chatdetail(room.id)
    else: #채팅방이 없다 -> 채팅방 생성, 회사의 안녕채팅 등록 -> 채팅방으로 이동
        room = Room(user_id = session['user_id'], company_id=company_id)
        db.session.add(room)
        db_room = Room.query.filter(Room.user_id==session['user_id'], Room.company_id==company_id).first()
        greetingchat1 = Chat(room_id=db_room.id, isuser=0, text=f'안녕하세요. {Company.query.get(company_id).companyname}입니다.')
        greetingchat2 = Chat(room_id=db_room.id, isuser=0, text=company_answer(db_room.id))
        db.session.add(greetingchat1)
        db.session.add(greetingchat2)
        db.session.commit()
        return chatdetail(db_room.id)
