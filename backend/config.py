class Config():
    DEBUG = False
    SQLALCHEMY_TRACE_MODIFICATIONS = False

class LocalDevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI= 'sqlite:///database.sqlite3'
    # SECURITY_KEY = 'super-security-key'
    # SECURITY_PASSWORD_SALT = 'super-security-salt'
    # WTF_CSRF_CHECK_DEFAULT = False
    # SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS = True
    # SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    # JWT_SECRET_KEY = 'sreedevi-is-my-gf'