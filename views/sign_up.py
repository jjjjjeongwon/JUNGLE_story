from flask import Blueprint, url_for, render_template, flash, request
from flask import redirect, session, g

from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from forms import UserCreateForm

import platform

current_operating_system = platform.system()
if current_operating_system == 'Windows' or current_operating_system == 'Darwin':
    client = MongoClient('localhost', 27017)
else:
    client = MongoClient('mongodb://asdf:asdf1234@localhost', 27017)
db = client.dbjungle

bp = Blueprint('sign_up', __name__, url_prefix='/sign_up')


@bp.route('/sign_up', methods=('GET', 'POST'))
def sign_up():
    form = UserCreateForm()

    if request.method == 'POST':

        user = db.user.find_one({'user_id': form.user_id.data})
        if user is None and form.validate_on_submit():
            new_user = {
                'user_id': form.user_id.data,
                'user_name': form.user_name.data,
                'password': generate_password_hash(form.password1.data)
            }
            db.user.insert_one(new_user)
            return redirect(url_for('root.root'))

    return render_template('sign_up.html', form=form)
