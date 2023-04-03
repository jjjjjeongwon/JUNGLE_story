from flask import Blueprint, url_for, render_template, flash, request
from flask import redirect, session, g
from datetime import datetime

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbjungle

bp = Blueprint('post_detail', __name__, url_prefix='/post_detail')


@bp.route('/<create_date>', methods=('GET', 'POST'))
def post_detail(create_date):

    post = db.post.find({'create_date': create_date})
    return render_template('post_detail.html', post=post)



