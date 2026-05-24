import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'online-ordering-secret-key')
    PERMANENT_SESSION_LIFETIME = timedelta(hours=4)

    # 优先使用 DATABASE_URL（云平台自动注入），否则使用 SQLite
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
