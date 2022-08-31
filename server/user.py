from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from app import db


class User(db.Model):
    __tablename__ = 'UserInfo'
    username = Column(String(20), primary_key=True)
    password = Column(String(20))
    viptype = Column(Integer)
    id = Column(String(20))
    tele = Column(String(20))
    validationcode = Column(String(20))

    def __init__(self, username, password, viptype, id, tele, validationcode):
        self.username = username
        self.password = password
        self.viptype = viptype
        self.id = id
        self.tele = tele
        self.validationcode = validationcode

class Staff(db.Model):
    __tablename__ = 'StaffInfo'
    staffid = Column(Integer, primary_key=True)
    name = Column(String(20))
    tele = Column(String(20))
    password = Column(String(20))
    position = Column(String(50))

    def __init__(self, staffid, name, tele, password, position):
        self.staffid = staffid
        self.name = name
        self.tele = tele
        self.password = password
        self.position = position

