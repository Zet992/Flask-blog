class Configuration:
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost/flaskdata"
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    SECRET_KEY = "secret key"

    SECURITY_PASSWORD_SALT = "salt"
    SECURITY_PASSWORD_HASH = "sha512_crypt"
    SECURITY_REGISTERABLE = True
    SECURITY_CONFIRMABLE = False

    UPLOAD_FOLDER = "app/static/profile_images/"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
