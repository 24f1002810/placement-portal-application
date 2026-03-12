class Config():
    DEBUG = False
    SQLALCHEMY_TRACE_MODIFICATIONS = False

class LocalDevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI= 'sqlite:///database.sqlite3'
    JWT_SECRET_KEY = 'sreedevi-is-my-gf'