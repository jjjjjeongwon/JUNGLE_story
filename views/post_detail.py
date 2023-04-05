from flask import Blueprint, url_for, render_template, flash, request, send_file
from flask import redirect, session, g
from datetime import datetime

from pymongo import MongoClient

import platform

current_operating_system = platform.system()
if current_operating_system == 'Windows' or current_operating_system == 'Darwin':
    client = MongoClient('localhost', 27017)
else:
    client = MongoClient('mongodb://asdf:asdf1234@localhost', 27017)

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
        db.post.update_one({"create_date": create_date}, {
                           "$set": {"like": post['like']}}, upsert=True)
    else:
        flash("이미 좋아요를 누르셨습니다.")
    return redirect(url_for('post_detail.post_detail', create_date=post['create_date']))


@bp.route('/delete/<create_date>')
def delete_posts(create_date):

    db.post.delete_one({'create_date': create_date})
    return redirect(url_for('post_list.post_list'))


@bp.route('/modify_onclick/<create_date>')
def modify_posts_onclick(create_date):
    post = db.post.find_one({'create_date': create_date})
    return render_template('post_modify.html', post=post)


@bp.route('/modify_work/<create_date>', methods=('GET', 'POST'))
def modify_posts_work(create_date):
    post = db.post.find_one({'create_date': create_date})

    title = request.args['post_title']
    content = request.args['post_content']

    db.post.update_one({'create_date': create_date}, {
        "$set": {
            "title": title,
            "content": content
        }
    })

    return redirect(url_for('post_detail.post_detail', create_date=post['create_date']))


@bp.route('/download/<create_date>', methods=('GET', 'POST'))
def download_file(create_date):

    post = db.post.find_one({'create_date': create_date})

    outputdata = post['file']

    print('ssdefds', outputdata)
    return send_file(outputdata, as_attachment=True)
