class Configuration:
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost/flaskdata"
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
