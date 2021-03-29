from flask import Blueprint, request, redirect, url_for, Response,render_template, session
# from twit_app.services import tweepy_api, embedding_api
# from twit_app.models import user_model, tweet_model
# from twit_app.services import tweepy_api, embedding_api
# from twit_app import db
# import re
# # from twit_app.services.embedding_api import get_embeddings

bp = Blueprint('find', __name__)

@bp.route('/find')
def findmain():
    print(session['user_id'],session['room_id'])
    return render_template('find.html')

# @bp.route('/user', methods=['POST'])
# def add_user():
#     """
#     add_user 함수는 JSON 형식으로 전달되는 폼 데이터로 유저를 트위터에서 조회한 뒤에
#     해당 유저와 해당 유저의 트윗들을 벡터화한 값을 데이터베이스에 저장합니다.
#     요구사항:
#       - HTTP Method: `POST`
#       - Endpoint: `api/user`
#       - 받는 JSON 데이터 형식 예시:
#             ```json
#             {
#                 "username":"업데이트할 유저의 username",
#                 "new_username":"새로 업데이트할 username"
#             }
#             ```
#     상황별 요구사항:
#       - 주어진 데이터에 `username` 키가 없는 경우:
#         - 리턴값: "Needs username"
#         - HTTP 상태코드: `400`
#       - 주어진 데이터의 `username` 에 해당하는 유저가 트위터에 존재하지 않은 경우:
#         - 리턴값: main_route.py 에 있는 user_index 함수로 리다이렉트 합니다.
#         - HTTP 상태코드: `400`
#      - 주어진 데이터의 `username` 을 가지고 있는 데이터가 이미 데이터베이스에 존재하는 경우:
#         - 해당 유저의 트윗 값들을 업데이트 합니다.
#         - 리턴값: main_route.py 에 있는 user_index 함수로 리다이렉트 합니다.
#         - HTTP 상태코드: `200`
#       - 정상적으로 주어진 `username` 을 트위터에서 가져오고 해당 유저의 트윗 또한 가져화 벡터화해서 데이터베이스에 기록한 경우:
#         - 리턴값: main_route.py 에 있는 user_index 함수로 리다이렉트 합니다.
#         - HTTP 상태코드: `200`
#     """
#     form = request.form
#     print(form)
#     username = form.get('username')
#     new_username=form.get('new_username')
    
#     if username  : # 입력이 있는경우
#       print('유저이름입력성공')
#       username = str(username).lower()
#       user_in_tweet = tweepy_api.get_user(username)
#       if user_in_tweet:# 트위터에 유저 존재하는 경우
#         t_followers = user_in_tweet.followers_count #팔로워수
#         t_full_name = user_in_tweet._json['name']
#         #입력의 유저 이름 db조회
#         user = user_model.User.query.filter(user_model.User.username == username).first()
        
#         if user : #기존에 존재하는 유저일 때
#           print('db_table User테이블에 이미 존재하는 유저')
#           ##- 해당유저의 트윗 값들 없데이트
#           user.full_name = t_full_name
#           user.followers = t_followers
#           ##-
#         else: #기존에 db에 존재하지 않는 유저일 때 :: 1. user생성  // 2. Tweet조회 & 크롤링 // 3. 저장  
#           print('db : User테이블에 존재하지 않으므로 , User를 생성합니다.')
#           user = user_model.User(username=username, full_name=t_full_name, followers=t_followers)
#           db.session.add(user)
#           print('User 생성 및 추가 완료')
        

#         ## tweet에서 유저 조회
#         t_tweets = tweepy_api.get_tweets(username)
        
#         ## db에 기존재하는 tweet들 가져와서 이걸 기준으로 새로운것들만 만들기
#         db_tweets_ids = [i.id for i in tweet_model.Tweet.query.filter(tweet_model.Tweet.user_id==user.id).all()]

#         ## Embeding값 받아오기
#         # re.sub('[^A-Za-z0-9가-힣]', '', string_text)   
#         # embed_results = embedding_api.get_embeddings(text_list=[re.sub('[^A-Za-z0-9가-힣]', ' ', i.text) for i in t_tweets])
#         if t_tweets is None:
#           print("That User doesn't have timeline, check the username")
#           return redirect(url_for('main.user_index', msg_code=0), code=200)
#         embed_results = embedding_api.get_embeddings(text_list=[re.sub('[^A-Za-z0-9가-힣]', ' ', i._json['full_text'].split('http')[0]) for i in t_tweets])
        
#         t_table_add_list = [] #Tweet table에 add할 유저
#         for timeline, embed in zip(t_tweets,embed_results):
#           #새로운 tweet과 id가 겹치는것 제외
#           if timeline.id in db_tweets_ids: continue
#           # t_table_add_list.append(tweet_model.Tweet(id=timeline.id ,text=timeline.text,user=user, embedding = embed))
#           t_table_add_list.append(tweet_model.Tweet(id=timeline.id ,text=timeline._json['full_text'],user=user, embedding = embed))
        
#         if t_table_add_list:
#           db.session.add_all(t_table_add_list)
#           print(len(t_table_add_list),'개의 트윗이 업데이트 되었습니다.')
        

#         ## DB에 저장 후 종료->리다이렉트
#         db.session.commit()
#         return redirect(url_for('main.user_index', msg_code=0), code=200)
#       else:
#         print('Tweet에 유저이름이 존재하지 않습니다')
#         return redirect(url_for('main.user_index', msg_code=0), code=400)
    
#     else:
#       print('유저이름없을때 -> error로 go')
#       return 'Needs username', 400

#     # full_name ## 트위터에서 가져와야함
#     return redirect(url_for('main.user_index', msg_code=0), code=200)




# @bp.route('/user/', methods = ['GET'])
# @bp.route('/user/<int:user_id>', methods=['GET'])
# def delete_user(user_id=None):
#     """
#     delete_user 함수는 `user_id` 를 엔드포인트 값으로 넘겨주면 해당 아이디 값을 가진 유저를 데이터베이스에서 제거해야 합니다.

#     요구사항:
#       - HTTP Method: `GET`
#       - Endpoint: `api/user/<user_id>`

#     상황별 요구사항:
#       -  `user_id` 값이 주어지지 않은 경우:
#         - 리턴값: 없음
#         - HTTP 상태코드: `400`
#       - `user_id` 가 주어졌지만 해당되는 유저가 데이터베이스에 없는 경우:
#         - 리턴값: 없음
#         - HTTP 상태코드: `404`
#       - 주어진 `username` 값을 가진 유저를 정상적으로 데이터베이스에서 삭제한 경우:
#         - 리턴값: main_route.py 에 있는 user_index 함수로 리다이렉트 합니다.
#         - HTTP 상태코드: `200`
#     """
#     # print("requestbutton : ", request.args , request.form)
#     # print('user_id : ',user_id)
#     user_id=request.args.get('user_id')
#     if user_id : 
#       print('user_id 입력 성공')
#       user = user_model.User.query.get(user_id)
#       if user : #user 가 db에 존재하는 경우
#         db.session.delete(user)
#         db.session.commit()
#         print('User delete 실행')
#         return redirect(url_for('main.user_index', msg_code=0), code=200)
#       else: # db에 존재하지 않음
#         print('선택한 user가 db에 존재하지 않습니다.')
#         return 'That User id is not in Database', 404
#     else:
#       print('user_id 가 없음')
#       return '유저아이디 입력이 없음', 400
