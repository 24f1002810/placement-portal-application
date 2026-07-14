class Config():
    DEBUG = False
    SQLALCHEMY_TRACE_MODIFICATIONS = False

class LocalDevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI= 'sqlite:///database.sqlite3'
    CELERY_BROKER_URL = 'redis://localhost:6379/1'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = "redis://localhost:6379/3"
    CACHE_DEFAULT_TIMEOUT = 180
    WEBHOOK_URL = 'https://script.google.com/macros/s/AKfycbxpIVV0-IdOl3CM7Twf-dptC2yNHTNADyJBkhlEVEL4MpEBjHUCaVnJwGvPfmeL1t3S/exec' # Replace with actual webhook url
    