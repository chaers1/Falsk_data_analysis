'''
项目数据库配置模块
'''
import os
import sys
import pymysql
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

'''数据库配置选项'''
pymysql.install_as_MySQLdb()  # 代替MySQLdb,使用pymysql

WIN = sys.platform.startswith('win')

if WIN:
    prefix = 'sqlite///'
else:
    prefix = 'sqlite////'

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:qazwsx%40123@127.0.0.1:3306/falsk_analysis'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)  # 封装flask实例到炼丹中
login_manager = LoginManager(app)  # 创建管理器实例


@login_manager.user_loader  # 指定函数加载用户，返回对象
def load_user(user_id):
    from core.models import Admin
    user = Admin.query.get(int(user_id))
    return user


login_manager.login_view = 'login'


from core import views