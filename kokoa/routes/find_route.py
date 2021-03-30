from flask import Blueprint, request, redirect, url_for, Response,render_template, session
# from twit_app.services import tweepy_api, embedding_api
# from twit_app.models import user_model, tweet_model
# from twit_app.services import tweepy_api, embedding_api
# from twit_app import db
# import re
# # from twit_app.services.embedding_api import get_embeddings

bp = Blueprint('find', __name__)

@bp.route('/find')
def findmain():#find의 메인 화면, user_id 동기화 확인 완료
    # print(session['user_id'],session['room_id'])

    return render_template('find.html')

