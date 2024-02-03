import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    BASE_DIR = basedir
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 10
    LANGUAGES = ['en', 'ru']
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'}
    MAX_CONTENT_LENGTH = 16 * 1000 * 1000
    UPLOAD = 'upload'