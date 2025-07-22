from app.modules.visual.route import visual_bp
from app.modules.chapter.route import chapter_bp
from app.modules.comic.route import comic_bp
from app.modules.like.route import like_bp
from flask import Flask
from flasgger import Swagger
from app.modules.main.route import main_bp
from app.db.db import db

def initialize_route(app: Flask):
    with app.app_context():
        app.register_blueprint(visual_bp, url_prefix='/api/v1/visual')
        app.register_blueprint(chapter_bp, url_prefix='/api/v1/chapter')
        app.register_blueprint(comic_bp, url_prefix='/api/v1/comic')
        app.register_blueprint(like_bp, url_prefix='/api/v1/like')
        app.register_blueprint(main_bp, url_prefix='/api/v1/main')


def initialize_db(app: Flask):
    with app.app_context():
        db.init_app(app)
        db.create_all()

def initialize_swagger(app: Flask):
    with app.app_context():
        swagger = Swagger(app)
        return swagger