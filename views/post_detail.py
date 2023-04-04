from flask import Blueprint, url_for, render_template, flash, request
from flask import redirect, session, g
from datetime import datetime

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbjungle
bp = Blueprint('post_detail', __name__, url_prefix='/post_detail')


@bp.route('/<create_date>', methods=('GET', 'POST'))
def post_detail(create_date):

    post = db.post.find_one({'create_date': create_date})
    return render_template('post_detail.html', post=post)


@bp.route('/like/<create_date>', methods=('GET', 'POST'))
def like(create_date):
    post = db.post.find_one({'create_date': create_date})
    user_id = g.user['user_id']

    if user_id not in post['like']:
        post['like'].append(user_id)
        db.post.update_one({"create_date": create_date}, {"$set": {"like": post['like']}}, upsert=True)
    else:
        flash("이미 좋아요를 누르셨습니다.")
    return render_template('post_detail.html', post=post)
