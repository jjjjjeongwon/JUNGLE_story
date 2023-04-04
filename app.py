from flask import Flask
from pymongo import MongoClient
from flask_jwt_extended import *

import config

client = MongoClient('localhost', 27017)
db = client.dbjungle


def create_app():
    app = Flask(__name__)

    app.config.from_object(config)
    app.config['JWT_SECRET_KEY'] = "yes"
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 900
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 180000
    app.config['JWT_BLACKLIST_ENABLED'] = True

    jwt = JWTManager(app)

    from views import root_views, sign_up, post_list, post_upload, post_detail, post_comment
    app.register_blueprint(root_views.bp)
    app.register_blueprint(sign_up.bp)
    app.register_blueprint(post_list.bp)
    app.register_blueprint(post_upload.bp)
    app.register_blueprint(post_detail.bp)
    app.register_blueprint(post_comment.bp)

    from filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    return app


if __name__ == '__main__':
    app = create_app()
    app.run('0.0.0.0', port=5000, debug=True)