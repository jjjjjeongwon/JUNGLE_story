from flask import Blueprint, url_for, render_template, flash, request, redirect, session, g, Response
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token
import jwt, platform
from pymongo import MongoClient

current_operating_system = platform.system()
if current_operating_system == 'Windows' or current_operating_system == 'Darwin':
    client = MongoClient('localhost', 27017)
else:
    client = MongoClient('mongodb://asdf:asdf1234@localhost', 27017)
db = client.dbjungle

from forms import UserLoginForm

bp = Blueprint('root', __name__, url_prefix='/')


@bp.route('/', methods=('GET', 'POST'))
def root():
    form = UserLoginForm()
    error = None

    if request.method == 'POST':
        user = db.user.find_one({'user_id': form.user_id.data})

        if user is None:
            error = "그런 사용자는 없습니다."
        elif not check_password_hash(user['password'], form.password.data):
            error = "비밀번호가 틀렸습니다."

        if error is None:
            session.clear()
            session['user_id'] = user['user_id']
            session['user_name'] = user['user_name']

            payload = {
                'id': user['user_id'],
                'exp': datetime.utcnow() + timedelta(seconds=60)
            }
            token = jwt.encode(payload, 'yes', algorithm='HS256')
            return redirect(url_for('post_list.post_list', access_token=token))
        else:
            flash(error)

        return render_template('root_views.html', form=form)
    else:
        list_user = list(db.user.find({}))
        return render_template('root_views.html', form=form, list_user=list_user)


@bp.route('/sign_up/', methods=('GET', 'POST'))
def sign_up():
    return redirect(url_for('sign_up.sign_up'))


@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('root.root'))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = db.user.find_one({'user_id': user_id})


def check_access_token(access_token):
    try:
        payload = jwt.decode(access_token, 'yes', "HS256")
        if payload['exp'] < datetime.utcnow():  # 토큰이 만료된 경우
            payload = None
    except jwt.InvalidTokenError:
        payload = None

    return payload


# decorator 함수
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwagrs):
        access_token = request.headers.get('Authorization')  # 요청의 토큰 정보를 받아옴
        if access_token is not None:  # 토큰이 있는 경우
            payload = check_access_token(access_token)  # 토큰 유효성 확인
            if payload is None:  # 토큰 decode 실패 시 401 반환
                return Response(status=401)
        else:  # 토큰이 없는 경우 401 반환
            return Response(status=401)

        return f(*args, **kwagrs)
    return decorated_function

