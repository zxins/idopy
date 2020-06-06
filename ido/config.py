DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASS = 'demo'
DB_PORT = 3306

SQLALCHEMY_DATABASE_URI = "mysql+cymysql://{0}:{1}@{2}:{3}/ido?charset=utf8".format(DB_USER, DB_PASS, DB_HOST, DB_PORT)

SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = "fasdfoijasdfjjfasdfkl"

WX_APPID = "wx150debc5513b84a6"
WX_SECRET = "c1fe849ff2278f3bb1b87ca1d053b4ba"