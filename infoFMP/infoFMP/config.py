class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://unisko:091517@localhost/demo'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    UPLOAD_FOLDER_IMG = 'images'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_POOL_SIZE = 10
    DEBUG = True
    SECRET_KEY = '\n\xd79\xf70\n\x1f\x80+Bv\xeb:\xd4k\x87\xe3\x97\x8f\x91\xff;\xda\x1a'
