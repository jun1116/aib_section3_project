class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite+pysqlite:///dev_db.sqlite3'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
        url="arjuna.db.elephantsql.com",user='puhxmtsx',pw='FlicJEXwJK-YRVaVQ9YcUrw43i0zGqHh',db='puhxmtsx')


class ProductionConfig(Config):
    # SQLALCHEMY_DATABASE_URI = 'sqlite+pysqlite:///prod_db.sqlite3'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
        url="arjuna.db.elephantsql.com",user='puhxmtsx',pw='FlicJEXwJK-YRVaVQ9YcUrw43i0zGqHh',db='puhxmtsx')

# 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
#     url="arjuna.db.elephantsql.com"
#     ,user='puhxmtsx'
#     ,pw='FlicJEXwJK-YRVaVQ9YcUrw43i0zGqHh'
#     ,db='puhxmtsx'
#     )