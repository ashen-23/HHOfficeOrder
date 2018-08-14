
SECRET_KEY = 'shmily'

DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = 'sj010606'
HOST = 'localhost'
PORT = '3306'
DATABASE = 'office'

# sqlalchemy 会自动在config中查找改变量名
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8mb4".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False
