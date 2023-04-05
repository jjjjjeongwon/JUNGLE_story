from flask import Blueprint, url_for, render_template, flash, request, jsonify
from flask import redirect, session, g
from datetime import datetime

import gridfs


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
        db.post.update_one({"create_date": create_date}, {
                           "$set": {"like": post['like']}}, upsert=True)
    else:
        flash("이미 좋아요를 누르셨습니다.")
    return redirect(url_for('post_detail.post_detail', create_date=post['create_date']))


@bp.route('/delete/<create_date>')
def delete_posts(create_date):

    db.post.delete_one({'create_date': create_date})
    return redirect(url_for('post_list.post_list'))


@bp.route('/download/<create_date>', methods=('GET', 'POST'))
def download_file(create_date):

    fs = gridfs.GridFS(db)

    post = db.post.find_one({'create_date': create_date})

    outputdata = fs.get(post['file'])

    # base64_img = codecs.encode(img_binary.read(), 'base64')

    # decode_img = base64_img.decode('utf-8')

    # post['file'] = decode_img

    # my_id = data['_id']
    # outputdata = fs.get(my_id).read()
    output = open('./images/'+'back.jpeg', 'wb')
    output.write(outputdata)
    return jsonify({'msg': '저장에 성공했습니다.'})




