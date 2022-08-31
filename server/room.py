from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, DATETIME
from sqlalchemy.ext.declarative import declarative_base
from app import db

class RoomInfo(db.Model):
    __tablename__ = 'RoomInfo'
    roomid = db.Column(db.String(20), primary_key=True)
    roomtype = Column(String(50))
    roomstate = Column(String(50))
    note = Column(String(255))

    def __init__(self, roomid, roomtype, roomstate, note):
        self.roomid = roomid
        self.roomtype = roomtype
        self.roomstate = roomstate
        self.note = note

    def to_dict(self):
        return {
            'roomid': self.roomid,
            'roomtype': self.roomtype,
            'roomstate': self.roomstate,
            'note': self.note
        }


class RoomType(db.Model):
    __tablename__ = 'RoomType'
    roomtype = Column(String(50), primary_key=True)
    price = Column(Integer)
    img = Column(String(255))

    def __init__(self, roomtype, price, img):
        self.roomtype = roomtype
        self.price = price
        self.img = img

class Booking(db.Model):
    __tablename__ = 'Booking'
    username = Column(String(20), primary_key=True)
    roomid = Column(String(20), primary_key=True)
    bookdate = Column(DATETIME, primary_key=True)
    fromdate = Column(DATETIME)
    todate = Column(DATETIME)
    isActive = Column(String(2))

    def __init__(self, username, roomid, bookdate, fromdate, todate, isActive):
        self.username = username
        self.roomid = roomid
        self.bookdate = bookdate
        self.fromdate = fromdate
        self.todate = todate
        self.isActive = isActive

class RoomState(db.Model):
    __tablename__ = 'RoomState'
    statename = Column(String(50), primary_key=True)
    isoccupied = Column(String(2))
    color = Column(String(255))

    def __init__(self, statename, isoccupied, color):
        self.statename = statename
        self.isoccupied = isoccupied
        self.color = color

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
