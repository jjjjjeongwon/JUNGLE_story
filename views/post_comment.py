from flask import Blueprint, url_for, render_template, flash, request
from flask import redirect, session, g
from datetime import datetime

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbjungle
bp = Blueprint('post_comment', __name__, url_prefix='/post_comment')


@bp.route('/create/<create_date>', methods=('GET', 'POST'))
def create(create_date):

    post = db.post.find_one({'create_date': create_date})

    user_id = g.user['user_id']
    user_name = g.user['user_name']
    post_id = post['_id']
    comment_content = request.form['commentContent']
    create_date = datetime.now().strftime('%Y%m%d%H%M%S')

    temp_comment = {
        'user_id': user_id,
        'user_name': user_name,
        'post_id': post_id,
        'comment_content': comment_content,
        'create_date': create_date,
        'modified_date': None
    }

    inserted_comment = db.comment.insert_one(temp_comment)
    comment_id = inserted_comment.inserted_id
    outed_comment = db.comment.find_one({'_id': comment_id})

    try:
        print(post['comment_set'])
        post['comment_set'].append(outed_comment)
    except Exception as e:
        post['comment_set'] = [outed_comment]

    db.post.update_one({"_id": post_id}, {"$set": {"comment_set": post['comment_set']}}, upsert=True)
    return redirect(url_for('post_detail.post_detail', create_date=post['create_date']))


@bp.route('/delete/<create_date>')
def delete(create_date):
    comment = db.comment.find_one({'create_date': create_date})
    post = db.post.find_one({'_id': comment['post_id']})
    post['comment_set'].remove(comment)

    db.comment.delete_one({'create_date': create_date})
    db.post.update_one({"_id": post['_id']}, {"$set": {"comment_set": post['comment_set']}}, upsert=True)
    return redirect(url_for('post_detail.post_detail', create_date=post['create_date']))


@bp.route('/modify_onclick/<create_date>')
def modify_onclick(create_date):
    comment = db.comment.find_one({'create_date': create_date})
    post = db.post.find_one({'_id': comment['post_id']})
    return render_template('comment_modify.html', comment=comment, post=post)


@bp.route('/modify_work/<create_date>', methods=['GET', 'POST'])
def modify_work(create_date):
    comment = db.comment.find_one({'create_date': create_date})
    new_content = request.form['new_content']
    db.comment.update_one({'create_date': create_date}, {'$set': {'comment_content': new_content}})

    post = db.post.find_one({'_id': comment['post_id']})

    post['comment_set'].remove(comment)
    comment['comment_content'] = new_content
    post['comment_set'].append(comment)
    id = post['_id']
    db.post.update_one({'create_date': post['create_date']}, {'$set': {'comment_set': post['comment_set']}})

    return redirect(url_for('post_detail.post_detail', create_date=post['create_date']))

