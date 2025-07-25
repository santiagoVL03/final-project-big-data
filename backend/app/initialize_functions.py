from app.modules.vistas_comic.route import vistas_comic_bp
from app.modules.get_comic_cover.route import get_comic_cover_bp
from app.modules.get_feed_mangas.route import get_feed_mangas_bp
from app.modules.upload_new_comic.route import upload_new_comic_bp
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
        app.register_blueprint(vistas_comic_bp, url_prefix='/api/v1/vistas_comic')
        app.register_blueprint(get_comic_cover_bp, url_prefix='/api/v1/get_comic_cover')
        app.register_blueprint(get_feed_mangas_bp, url_prefix='/api/v1/get_feed_mangas')
        app.register_blueprint(upload_new_comic_bp, url_prefix='/api/v1/upload_new_comic')
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