from flask import Blueprint, url_for, render_template, flash, request
from flask import redirect, session, g
from flask_jwt_extended import *
from datetime import datetime

from pymongo import MongoClient

from .root_views import login_required

client = MongoClient('localhost', 27017)
db = client.dbjungle

bp = Blueprint('post_list', __name__, url_prefix='/post_list')


@bp.route('/', methods=('GET', 'POST'))
def post_list():   
    token = request.args['access_token']
    postList = list(db.post.find({}).sort('create_date', -1))
    return render_template('post_list.html', post_list=postList, access_token=token), 200


@bp.route('/write_post')
def write_post():
    return redirect(url_for('post_upload.post_upload'))


@bp.route('/read_post/<create_date>/')
@login_required
def read_post(create_date=None):
    print("DEBUG DEBUG")
    print(create_date)
    return redirect(url_for('post_detail.post_detail'), create_date=create_date)

# @bp.route('/read_post/')
# def read_post():
#     print("DEBUG DEBUG")
#     return redirect(url_for('post_detail.post_detail'))


@bp.route('/write_sample_post')
@login_required
def write_sample_post():
    title = 'Sample Title'
    content = 'Sample content. 동해물과 백두산이 마르고 닳도록 하느님이 보우하사 우리 나라 만세\n \
                무궁화 삼천리 화려강산 대한사람 대한으로 길이 보전하세'
    uploaded_file = None
    author = '홍길동'
    create_date = datetime.now()
    file_url = 'static.image1.jpg'

    new_article = {
        'title': title,
        'content': content,
        'uploaded_file': uploaded_file,
        'author': author,
        'create_date': create_date,
        'file': file_url
    }

    res = db.post.insert_one(new_article)
    print(res)
    print(res.inserted_id)

    return redirect(url_for('post_list.post_list'))
