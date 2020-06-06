from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, VARCHAR, Integer, TEXT
from ido import utils

db = SQLAlchemy()


class Members(db.Model):
    id = Column(Integer, primary_key=True, unique=True)
    openid = Column(VARCHAR(100), nullable=False, unique=True, comment='openid')
    name = Column(VARCHAR(50), nullable=False, comment='用户昵称')
    face = Column(VARCHAR(200), nullable=False, comment='用户头像')
    random = Column(VARCHAR(30), comment='用户随机码')
    integral = Column(Integer, default=0, comment='积分')
    remainder = Column(Integer, default=0, comment='余额')
    regtime = Column(Integer, default=utils.timestamp(), comment='注册时间')

    def just_add(self):
        db.session.add(self)

    def save(self):
        db.session.add(self)
        db.session.commit()


class AccessTokens(db.Model):
    id = Column(Integer, primary_key=True)
    token = Column(VARCHAR(30), nullable=False)
    time = Column(Integer, )

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Categories(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, nullable=False)
    name = Column(VARCHAR(50))
    order = Column(Integer)


class Articles(db.Model):
    id = Column(Integer, primary_key=True)
    cate = Column(Integer)
    title = Column(VARCHAR(200))
    uid = Column(Integer, db.ForeignKey('members.id'))
    content = Column(TEXT, nullable=False)
    create_time = Column(Integer, default=utils.timestamp())

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()