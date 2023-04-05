import os
import gridfs
from flask import Blueprint, url_for, render_template, flash, request
from flask import redirect, session, g

from datetime import datetime

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbjungle

UPLOAD_FOLDER = os.getcwd() + '\\upload'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

UPLOAD_FILE = None

bp = Blueprint('post_upload', __name__, url_prefix='/post_upload')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@bp.route('/', methods=('POST', 'GET'))
def post_upload():

    global UPLOAD_FILE

    if request.method == 'POST':

        post_file = request.files['post_file']
        print('테스트 프린트', post_file)

        post_title = request.form['post_title']
        post_content = request.form['post_content']

        today = datetime.now()
        today = today.strftime('%Y%m%d%H%M%S')

        fs = gridfs.GridFS(db)
        file_img_id = fs.put(post_file, filename=today)

        print(file_img_id)

        new_post = {
            'title': post_title,
            'content': post_content,
            'file': file_img_id,
            'create_date': today,
            'user_id': g.user['user_id'],
            'user_name': g.user['user_name'],
            'like': [],
            'comment_set': []
        }

        db.post.insert_one(new_post)

        return redirect(url_for('post_list.post_list'))

    return render_template('post_upload.html')


@bp.route('/modifying/<create_date>', methods=('GET', 'POST'))
def post_modify(create_date):
    post = db.post.find_one({'create_date': create_date})

    if request.method == "POST":
        title = request.form['post_title']
        content = request.form['post_content']
        post.update_one({'create_date': create_date}, {
            "$set": {
                "title": title,
                "content": content
            }
        })

        return redirect(url_for('post_list.post_list'))

    return render_template('post_upload.html')
