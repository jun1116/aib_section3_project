# # config.py
# db = {
#     'user'     : 'root',		# 1)
#     'password' : '0000',		# 2)
#     'host'     : 'localhost',	# 3)
#     'port'     : 3306,			# 4)
#     'database' : 'kokoa'		# 5)
# }
# SQLALCHEMY_DATABASE_URI: postgresql://username:password@localhost:5432/dbname
# DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite+pysqlite:///dev_db.sqlite3'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite+pysqlite:///prod_db.sqlite3'
