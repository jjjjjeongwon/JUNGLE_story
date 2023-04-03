from flask import Blueprint, url_for, render_template, flash, request
from flask import redirect, session, g

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbjungle

bp = Blueprint('post_upload', __name__, url_prefix='/post_upload')


@bp.route('/', methods=('GET', 'POST'))
def post_upload():   
    return render_template('post_upload.html')


