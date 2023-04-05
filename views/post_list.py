from flask import Blueprint, url_for, render_template, flash, request
from flask import redirect, session, g
from flask_jwt_extended import *
from datetime import datetime

from pymongo import MongoClient

import copy, jwt

# from .root_views import login_required

client = MongoClient('localhost', 27017)
db = client.dbjungle

bp = Blueprint('post_list', __name__, url_prefix='/post_list')


@bp.route('/', methods=('GET', 'POST'))
def post_list():

    print(request.method)

    if request.form.keys():
        kw = request.form['kw']
    else:
        kw = ''

    postList = list(db.post.find({}).sort('create_date', -1))
    list_user = list(db.user.find({}))
    list_user = renewal_user_list(list_user)

    if kw:
        user = db.user.find_one({'user_id': kw})
        if user is not None:
            return select_user(user['user_id'])

        user = db.user.find_one({'user_name': kw})
        if user is not None:
            return select_user(user['user_id'])
    else:
        return select_user(g.user['user_id'])

    return render_template('post_list.html', post_list=postList, list_user=list_user), 200


@bp.route('/write_post')
def write_post():
    return redirect(url_for('post_upload.post_upload'))


@bp.route('/read_post/<create_date>/')
def read_post(create_date):
    return redirect(url_for('post_detail.post_detail', create_date=create_date))


@bp.route('/select_user/<user_id>')
def select_user(user_id):
    postList = list(db.post.find({}).sort('create_date', -1))

    list_user = list(db.user.find({}))
    list_user = renewal_user_list(list_user)
    selected_user = db.user.find_one({'user_id': user_id})

    user_post_list = copy.deepcopy(postList)

    for post in postList:
        if post['user_id'] != selected_user['user_id']:
            user_post_list.remove(post)

    return render_template('post_list.html', post_list=postList, list_user=list_user,
                           selected_user=selected_user, user_post_list=user_post_list), 200


@bp.route('/root/write_sample_post')
def write_sample_post():
    user_id = 'q@q.q'
    user_name = 'q'
    title = 'Sample Title'
    content = 'Sample content. 동해물과 백두산이 마르고 닳도록 하느님이 보우하사 우리 나라 만세\n \
                무궁화 삼천리 화려강산 대한사람 대한으로 길이 보전하세'
    uploaded_file = None
    create_date = datetime.now()
    file_url = 'static.image1.jpg'

    create_date = create_date.strftime('%Y%m%d%H%M%S')

    new_post = {
        'title': title,
        'content': content,
        'user_id': user_id,
        'user_name': user_name,
        'create_date': create_date,
        'file': file_url
    }

    inserted_user = db.post.insert_one(new_post)
    id = inserted_user.inserted_id
    new_post['primary_key'] = id
    db.post_with_id.insert_one(new_post)

    return redirect(url_for('post_list.post_list'))


@bp.route('/root/set_post_like_0')
def set_post_like_0():
    posts = list(db.post.find({}))

    for post in posts:
        try:
            print(post['like'])
        except KeyError as e:
            post['like'] = 0

    db.post.delete_many({})

    for post in posts:
        db.post.insert_one(post)

    return redirect(url_for('post_list.post_list'))


@bp.route('/root/set_post_name_q')
def set_post_name_q():
    posts = list(db.post.find({}))
    for post in posts:
        try:
            print(post['user_name'])
        except KeyError as e:
            post['user_name'] = 'q'

        try:
            print(post['user_id'])
        except KeyError as e:
            print("SET POST'S USER_ID")
            post['user_id'] = 'q@q.q'

    db.post.delete_many({})
    for post in posts:
        db.post.insert_one(post)

    return redirect(url_for('post_list.post_list'))


def renewal_user_list(list_user):

    postList = list(db.post.find({}).sort('create_date', -1))
    now_user = db.user.find_one({'user_id': g.user['user_id']})

    for user in list_user:
        try:
            a = user['user_id']
        except KeyError as e:
            list_user.remove(user)

    for user in list_user:
        user['entire_like'] = 0
    now_user['entire_like'] = 0

    # list_user.remove(now_user)

    for post in postList:
        for like_user in post['like']:
            for user in list_user:
                if like_user == user['user_id']:
                    user['entire_like'] = user['entire_like'] + 1

    list_user = sorted(list_user, key=lambda x: -x['entire_like'])
    return list_user


def test_list():
    return [11, 22, 33, 44, 55]