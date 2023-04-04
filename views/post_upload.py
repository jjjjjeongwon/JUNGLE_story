from flask import Blueprint, url_for, render_template, flash, request
from flask import redirect, session, g

from datetime import datetime

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbjungle

bp = Blueprint('post_upload', __name__, url_prefix='/post_upload')


@bp.route('/', methods=('POST', 'GET'))
def post_upload():
    if request.method == 'POST':
        post_title = request.form['post_title']
        post_content = request.form['post_content']
        post_file = request.form['post_file']

        today = datetime.now()

        new_post = {
            'title': post_title,
            'content': post_content,
            'file': post_file,
            'create_date': today,
            'author': g.user['user_id']
        }

        res = db.post.insert_one(new_post)
        print(new_post)
        print(res)

    return render_template('post_upload.html')
