from flask import Blueprint, render_template, request, session, url_for
from kokoa.models.user_model import User, Company, Room, Chat
from kokoa import db

bp = Blueprint('chat',__name__)

@bp.route('/chats/')#채팅방리스트 페이지(chats)
def chats():
    user_id = session['user_id']
    user = User.query.get(user_id)
    rooms = Room.query.filter(Room.user_id==user_id).all()
    print('userid : ',user_id,'\tUSER : ', user)
    print('ROOMS : ',rooms)
    roomList = []
    for room in rooms:
        roomList.append({'company_name':Company.query.get(room.company_id).companyname,'text':"check", 'room_id':room.id })
    return render_template('chats.html', roomlist=roomList)

@bp.route('/chatdetail/<int:room_id>')#주고받은 메시지 띄울 페이지
def chatdetail(room_id):
    room = Room.query.get(room_id)
    chats = Chat.query.filter(Chat.room_id==room_id).all()
    company = Company.query.get(room.company_id)
    print(chats)
    session['room_id']=room.id
    return render_template('chatdetail.html',companyname=company.companyname ,room=room,chats=chats)

@bp.route('/chatdetail/', methods=['POST'])
def reply():
    form = request.form
    text = form['reply']
    print('세션에 남은 유저아이디',session['user_id'])
    print('세션에 남은 룸아이디',session['room_id'])
    # print(data)
    db.session.add(Chat(room_id=session['room_id'], text=text, isuser=1))
    db.session.commit()
    return chatdetail(session['room_id'])

