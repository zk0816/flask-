# coding=utf8
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import pymysql
from datetime import datetime

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:88888888@192.168.159.130:3306/test'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + './sec.db/'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET KEY'] = 'gjhkghkgkgk'
app.secret_key = 'dafafadada'  # 唯一的key

db = SQLAlchemy(app)


# 管理员
class Admim(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)  # 主键
    username = db.Column(db.String(32), nullable=False, unique=True)  # 账号
    password = db.Column(db.String(64), nullable=False)  # 密码
    tags = db.relationship('Tag', backref='admin')  # 一对多


# 用户
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)  # 主键
    username = db.Column(db.String(32), nullable=False, unique=True)  # 账号
    password = db.Column(db.String(64), nullable=False)  # 密码
    messages = db.relationship('Message', backref='user')


# 留言条
class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)  # 主键
    content = db.Column(db.String(255), nullable=False)  # 内容
    create_time = db.Column(db.DateTime, default=datetime.now())  # 发布留言的时间
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    tag = db.relationship('Tag', secondary='message_to_tag', backref='messages')  # 关系关联


# 标签
class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(10), nullable=False)  # 标签名字
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员


# 中间表
class MessageToTag(db.Model):
    __tablename__ = 'message_to_tag'
    id = db.Column(db.Integer, primary_key=True)  # 主键
    message_id = db.Column(db.Integer, db.ForeignKey('message.id',ondelete='CASCADE'))  # 所属留言条
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id',ondelete='CASCADE'))  # 所属标签


if __name__ == '__main__':
    db.create_all()
    # db.drop_all()
