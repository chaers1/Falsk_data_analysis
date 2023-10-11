from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from core import db

'''数据库注册'''


class Admin(db.Model, UserMixin):
    __tablename__ = 'flask_analysis_admin'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    flasktime = db.Column(db.DateTime)

    def set_pwd(self, mpassword):  # 密码加密函数
        self.password = generate_password_hash(mpassword)

    def validate_pwd(self, ypassword):  # 密码解密函数
        return check_password_hash(self.password, ypassword)


'''电商数据表格数据组orm'''


class Table(db.Model):
    __tablename__ = 'flask_analysis_biaoge'
    id = db.Column(db.Integer, primary_key=True)  # id 自增
    produtc_code = db.Column(db.String(255), nullable=True)  # 货号
    sale_data = db.Column(db.DateTime, nullable=True)  # 销售日期
    customer_counts = db.Column(db.Integer, nullable=True)  # 客户数
    tltal_sales = db.Column(db.Float, nullable=True)  # 销售额
    total_quantity = db.Column(db.Integer, nullable=True)  # 销售量
    sales_after_discount = db.Column(db.Float, nullable=True)  # 销售额含满减拒退
    uv = db.Column(db.Integer, nullable=True)  # uv
    conversion_rate = db.Column(db.Float, nullable=True)  # 转化率
    product_ctr = db.Column(db.Float, nullable=True)  # 商品ctr
    exposure_uv = db.Column(db.Float, nullable=True)  # 曝光uv
    style_code_auxiliary = db.Column(db.String(255), nullable=True)  # 款号辅助
    sales_range = db.Column(db.String(255), nullable=True)  # 销售区间
    category = db.Column(db.String(255), nullable=True)  # 品类
    activity = db.Column(db.String(255), nullable=True)  # 活动
    net_price = db.Column(db.Float, nullable=True)  # 到手价
    net_price_range = db.Column(db.String(255), nullable=True)  # 到手价区间
