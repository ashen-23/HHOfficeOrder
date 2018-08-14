from exts import db
from jieba.analyse.analyzer import ChineseAnalyzer


# 办公室
class OfficeModel(db.Model):
    __tablename__ = 'office'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 名称
    name = db.Column(db.String(100), nullable=False)

    # 描述
    desc = db.Column(db.String(100), nullable=False)


class OrderModel(db.Model):
    __tablename__ = 'order'

    __searchable__ = ['user_name', 'depart_name', 'reason']
    __analyzer__ = ChineseAnalyzer()

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 预订人
    user_name = db.Column(db.String(100), nullable=False)
    depart_name = db.Column(db.String(100), nullable=False)

    # 预订原因
    reason = db.Column(db.Text, nullable=False)

    office_id = db.Column(db.Integer, db.ForeignKey('office.id'))
    office = db.relationship('OfficeModel', backref=db.backref('orders'))

    # 预订时间
    order_from = db.Column(db.Integer, nullable=False)
    order_to = db.Column(db.Integer, nullable=False)
    # 当天0点时间戳
    order_day = db.Column(db.Integer, nullable=False)

    def to_dict(self, **args):
        base_arg = {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
        return dict(base_arg, **args)