import codecs
import csv
import os
import random
import uuid
from curses.ascii import isdigit
from datetime import datetime, timedelta

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import jwt

from functools import wraps

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, Column, Integer, String, DATETIME, or_, Float, desc

from dbutil import DatabaseManagement

from flask_mail import Message, Mail

import _thread
import time

key = '123456'

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(
    # 邮箱配置
    # MAIL_USE_TLS：端口号587
    # MAIL_USE_SSL：端口号465
    # QQ邮箱不支持非加密方式发送邮件
    # 发送者邮箱的服务器地址
    MAIL_SERVER="smtp.qq.com",
    MAIL_PORT='587',
    MAIL_USE_TLS=True,
    # MAIL_USE_SSL
    MAIL_USERNAME="owiefvdfn@qq.com",
    MAIL_PASSWORD="ndpevnwlgrqkbfbj",  # 生成授权码，授权码是开启smtp服务后给出的
    MAIL_DEFAULT_SENDER="owiefvdfn@qq.com",
)


mail = Mail(app)

CORS(app)

# 配置数据库的连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pymssql://sa:ilovelq@1.117.228.153/HotelManagement'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'UserInfo'
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(20))
    viptype = db.Column(db.Integer)
    id = db.Column(db.String(20))
    tele = db.Column(db.String(20))
    validationcode = db.Column(db.String(20))

    def __init__(self, username, password, viptype, id, tele, validationcode):
        self.username = username
        self.password = password
        self.viptype = viptype
        self.id = id
        self.tele = tele
        self.validationcode = validationcode

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
            'viptype': self.viptype,
            'id': self.id,
            'tele': self.tele,
            'validationcode': self.validationcode
        }

class Staff(db.Model):
    __tablename__ = 'StaffInfo'
    staffid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    tele = db.Column(db.String(20))
    password = db.Column(db.String(20))
    position = db.Column(db.String(50))

    def __init__(self, staffid, name, tele, password, position):
        self.staffid = staffid
        self.name = name
        self.tele = tele
        self.password = password
        self.position = position

class RoomInfo(db.Model):
    __tablename__ = 'RoomInfo'
    roomid = db.Column(db.String(20), primary_key=True)
    roomtype = Column(String(50))
    roomstate = Column(String(50))
    note = Column(String(255))
    username = db.Column(db.String(20))

    def __init__(self, roomid, roomtype, roomstate, note, username=''):
        self.roomid = roomid
        self.roomtype = roomtype
        self.roomstate = roomstate
        self.note = note
        self.username = username

    def to_dict(self):
        return {
            'roomid': self.roomid,
            'roomtype': self.roomtype,
            'roomstate': self.roomstate,
            'note': self.note,
            'username': self.username
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

    def to_dict(self):
        return {
            'roomtype': self.roomtype,
            'price': self.price,
            'img': self.img,
            'number': 0
        }

class Booking(db.Model):
    __tablename__ = 'Booking'
    username = Column(String(20), primary_key=True)
    roomid = Column(String(20), primary_key=True)
    bookdate = Column(DATETIME, primary_key=True)
    fromdate = Column(DATETIME)
    todate = Column(DATETIME)
    isActive = Column(String(2))
    money = Column(Float)

    def __init__(self, username, roomid, bookdate, fromdate, todate, isActive, money):
        self.username = username
        self.roomid = roomid
        self.bookdate = bookdate
        self.fromdate = fromdate
        self.todate = todate
        self.isActive = isActive
        self.money = money

    def to_dict(self):
        return {
            'username': self.username,
            'roomid': self.roomid,
            'bookdate': self.bookdate,
            'fromdate': self.fromdate,
            'todate': self.todate,
            'isActive': self.isActive,
            'money': self.money
        }

class RoomState(db.Model):
    __tablename__ = 'RoomState'
    statename = Column(String(50), primary_key=True)
    isoccupied = Column(String(4))
    color = Column(String(255))

    def __init__(self, statename, isoccupied, color):
        self.statename = statename
        self.isoccupied = isoccupied
        self.color = color

    def to_dict(self):
        return {
            'statename': self.statename,
            'isoccupied': self.isoccupied,
            'color': self.color,
            'number': 0
        }

def generate_access_token(username: str = '', algorithm: str = 'HS256', exp: float = 2):
    """
    Generate access token
    """
    now = datetime.utcnow()
    exp_datetime = now + timedelta(hours=exp)
    access_payload = {
        'exp': exp_datetime,
        'flag': 0,  # 是否为一次性token 0 是 1 不是
        'iat': now,
        'iss': 'ilovelq',
        'username': username
    }
    access_token = jwt.encode(access_payload, key, algorithm=algorithm)
    return access_token

def decode_auth_token(token: str):
    """
    Decode access token
    """
    try:
        payload = jwt.decode(token, key, algorithms='HS256')
        return payload
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'


def identify(auth_header: str):
    """
    Identify user
    """
    if auth_header:
        payload = decode_auth_token(auth_header)
        if not payload:
            return False
        if "username" in payload and "flag" in payload:
            if payload["flag"] == 0:
                return payload["username"]
            else:
                return False
    return False


def login_required(f):
    """
    Login required decorator
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization', default=None)
        if not token:
            return 'Not Login', '403 Permission Denied'
        username = identify(token)
        if not username:
            return 'Not Login', '403 Permission Denied'
        return f(*args, **kwargs)

    return decorated_function


@app.route('/api/login', methods=['POST', 'GET'])
def verify_login():
    if request.method == 'GET':
        return jsonify({
            'code': -1
        })
    username = request.json.get('username')
    pwd = request.json.get('password')
    print(username, pwd)
    userinfo = User.query.filter_by(username=username).first()

    staff = None
    if isdigit(username[len(username) - 1]):
        staff = Staff.query.filter_by(staffid=int(username)).first()

    if userinfo:
        # userinfo = userinfo[0]
        if username == userinfo.username.strip() and pwd == userinfo.password.strip():
            return jsonify({
                'code': 0,
                'token': generate_access_token(username),
                'user': username,
                'type': 'user'
            })

    if staff:
        # staff = staff[0]
        if username == str(staff.staffid) and pwd == staff.password.strip():
            return jsonify({
                'code': 0,
                'token': generate_access_token(username),
                'user': username,
                'type': 'staff'
            })

    return jsonify({
        'code': -1,
        'msg': '用户名或密码错误'
    })

@app.route('/api/register', methods=['POST'])
def register():
    username = request.json.get('username')

    userinfo = User.query.filter_by(username=username).all()
    if userinfo:
        return jsonify({
            'code': -1,
            'msg': '用户名已存在'
        })

    pwd = request.json.get('password')
    id = request.json.get('id')
    phone = request.json.get('phone')

    # insert user
    user = User(username=username, password=pwd, id=id, viptype=1, tele=phone, validationcode='none')
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'code': 0
    })

def delete_user(username: str):
    time.sleep(120)
    user = User.query.filter_by(username=username).first()
    if user.validationcode != 'done':
        db.session.delete(user)
        db.session.commit()

@app.route('/api/send_code', methods=['GET', 'POST'])
def send_code():
    msg_title = '客房管理系统的验证码'
    #  收件者，格式為list，否則報錯
    msg_recipients = [ request.json.get('username')]
    #  郵件內容
    captcha = str(uuid.uuid1())[:6]  # 随机生成6位验证码
    # 给用户提交的邮箱发送邮件
    msg_body = '您的验证码是：%s' % captcha + '，请在2分钟内完成验证。'
    #  也可以使用html
    #  msg_html = '<h1>Hey,Flask-mail Can Use HTML</h1>'
    msg = Message(msg_title,
                  recipients=msg_recipients)
    msg.body = msg_body
    #  msg.html = msg_html

    #  mail.send:寄出郵件
    mail.send(msg)

    username = request.json.get('username')
    userinfo = User.query.filter_by(username=username).first()
    if userinfo:
        userinfo.validationcode = captcha
        db.session.commit()
        if not request.json.get('change'):
            print('start thread')
            # _thread.start_new_thread(delete_user, (username,))

    return jsonify({
        'code': 0
    })

@app.route('/api/validate_code', methods=['GET', 'POST'])
def validate_code():
    username = request.json.get('username')
    code = request.json.get('code')
    userinfo = User.query.filter_by(username=username).first()
    if userinfo:
        if userinfo.validationcode == code:
            userinfo.validationcode = 'done'
            db.session.commit()
            return jsonify({
                'code': 0
            })
    return jsonify({
        'code': -1,
        'msg': '验证码错误'
    })

@app.route('/image/room/<imageid>.jpeg', methods=['GET', 'POST'])
def get_image(imageid):
    print(imageid)
    with open('./image/room/' + imageid + '.jpeg', 'rb') as f:
        image = f.read()
        return Response(image, mimetype="image/jpeg")

@app.route('/test')
def test():
    return 'test'

@app.route('/api/get_room_list', methods=['GET', 'POST'])
def get_room_list():
    room_list = RoomInfo.query.all()
    data = [room.to_dict() for room in room_list]
    # print(data)
    return jsonify({
        'code': 0,
        'data': data
    })

@app.route('/api/get_room_state', methods=['GET', 'POST'])
def get_room_state():
    room_state_list = db.session.query(RoomState).all()
    data = [room_state.to_dict() for room_state in room_state_list]
    return jsonify({
        'code': 0,
        'data': data
    })

@app.route('/api/get_room_type', methods=['GET', 'POST'])
def get_room_type():
    room_type_list = db.session.query(RoomType).all()
    data = [room_type.to_dict() for room_type in room_type_list]
    return jsonify({
        'code': 0,
        'data': data
    })

def _get_availiable_room(check_in_time, check_out_time):
    room_list = RoomInfo.query.all()

    availiable_room = []

    for room in room_list:
        room_bookings = db.session.query(Booking) \
            .filter(Booking.roomid == room.roomid) \
            .filter(or_(and_(Booking.fromdate < check_in_time, Booking.todate > check_in_time),
                        and_(Booking.fromdate < check_out_time, Booking.todate > check_out_time))) \
            .all()
        if not room_bookings:
            availiable_room.append(room)

    return availiable_room

@app.route('/api/get_availiable_room', methods=['GET', 'POST'])
def get_availiable_room():
    check_in_date = request.json.get('check_in_date')
    check_out_date = request.json.get('check_out_date')

    check_in_time = check_in_date + ' 00:00:00'
    check_out_time = check_out_date + ' 00:00:00'

    availiable_room = [room.to_dict() for room in _get_availiable_room(check_in_time, check_out_time)]

    return jsonify({
        'code': 0,
        'data': availiable_room
    })

@app.route('/api/get_availiable_room_type', methods=['GET', 'POST'])
def get_availiable_room_type():
    check_in_date = request.json.get('check_in_date')
    check_out_date = request.json.get('check_out_date')

    print(check_out_date)

    check_in_time = check_in_date + ' 00:00:00'
    check_out_time = check_out_date + ' 00:00:00'

    availiable_room = _get_availiable_room(check_in_time, check_out_time)

    room_type_list = RoomType.query.all()
    room_type_number = {}

    for room_type in room_type_list:
        room_type_number[room_type.roomtype] = 0
        print(room_type.roomtype)

    for room in availiable_room:
        room_type_number[room.roomtype] += 1

    room_type_list = [room_type.to_dict() for room_type in room_type_list]

    for room_type in room_type_list:
        room_type['number'] = room_type_number[room_type['roomtype']]

    # print(room_type_list)

    return jsonify({
        'code': 0,
        'data': room_type_list
    })

@app.route('/api/make_room_busy', methods=['GET', 'POST'])
def make_room_busy():
    roomid = request.json.get('roomid')
    room = RoomInfo.query.filter_by(roomid=roomid).first()
    room.roomstate = '正在处理'
    db.session.commit()

    return jsonify({
        'code': 0
    })

@app.route('/api/make_room_free', methods=['GET', 'POST'])
def make_room_free():
    roomid = request.json.get('roomid')
    room = RoomInfo.query.filter_by(roomid=roomid).first()
    room.roomstate = '空闲'
    db.session.commit()

    return jsonify({
        'code': 0
    })

@app.route('/api/add_room', methods=['GET', 'POST'])
def add_room():
    roomid = request.json.get('roomid')
    roomtype = request.json.get('roomtype')
    roomstate = request.json.get('roomstate')
    note = request.json.get('note')

    room = RoomInfo(roomid, roomtype, roomstate, note)
    db.session.add(room)
    db.session.commit()

    return jsonify({
        'code': 0
    })

# delete room
@app.route('/api/delete_room', methods=['GET', 'POST'])
def delete_room():
    roomid = request.json.get('roomid')

    room = RoomInfo.query.filter_by(roomid=roomid).first()
    db.session.delete(room)
    db.session.commit()

    return jsonify({
        'code': 0
    })

# edit room
@app.route('/api/edit_room', methods=['GET', 'POST'])
def edit_room():
    roomid = request.json.get('roomid')
    roomtype = request.json.get('roomtype')
    roomstate = request.json.get('roomstate')
    note = request.json.get('note')

    room = RoomInfo.query.filter_by(roomid=roomid).first()
    room.roomtype = roomtype
    room.roomstate = roomstate
    room.note = note

    db.session.commit()

    return jsonify({
        'code': 0
    })

# get bookings
@app.route('/api/get_booking', methods=['GET', 'POST'])
def get_booking():
    booking_list = db.session.query(Booking).order_by(desc(Booking.bookdate)).all()
    data = [booking.to_dict() for booking in booking_list]
    return jsonify({
        'code': 0,
        'data': data
    })

@app.route('/api/get_user_booking', methods=['GET', 'POST'])
def get_user_booking():
    username = request.json.get('username')
    username = username
    # print(username)
    booking_list = db.session.query(Booking).filter_by(username=username).order_by(desc(Booking.bookdate)).all()
    data = [booking.to_dict() for booking in booking_list]
    # print(data)
    return jsonify({
        'code': 0,
        'data': data
    })

def _cal_day_(fromdate, todate):
    fromdate = datetime.strptime(fromdate, '%Y-%m-%d')
    todate = datetime.strptime(todate, '%Y-%m-%d')

    day_number = (todate - fromdate).days

    return day_number

@app.route('/api/get_day_money', methods=['GET', 'POST'])
def get_day_money():
    room_type = request.json.get('roomtype')
    check_in_date = request.json.get('check_in_date')
    check_out_date = request.json.get('check_out_date')

    if not room_type:
        room_id = request.json.get('roomid')
        room_type = RoomInfo.query.filter_by(roomid=room_id).first().roomtype

    num = _cal_day_(check_in_date, check_out_date)
    price = RoomType.query.filter_by(roomtype=room_type).first().price * num

    return jsonify({
        'code': 0,
        'price': price,
        'num': num,
        'roomtype': room_type
    })

@app.route('/api/add_booking', methods=['GET', 'POST'])
def add_booking():
    username = request.json.get('username')
    roomid = request.json.get('roomid')
    roomtype = request.json.get('roomtype')
    fromdate = request.json.get('fromdate')
    todate = request.json.get('todate')
    isActive = request.json.get('isActive')

    room = None

    if not roomid or roomid == '':
        # random room of room list
        room = RoomInfo.query.filter_by(roomtype=roomtype).all()
        room = random.choice(room)
        roomid = room.roomid
    else:
        room = RoomInfo.query.filter_by(roomid=roomid).first()
        roomtype = RoomInfo.query.filter_by(roomid=roomid).first().roomtype

    num = _cal_day_(fromdate, todate)

    # money = request.json.get('money')
    price = RoomType.query.filter_by(roomtype=roomtype).first().price
    money = price * num

    booking = Booking(username, roomid, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), fromdate, todate, isActive, money)
    db.session.add(booking)
    room.roomstate = '被预定'
    db.session.commit()

    return jsonify({
        'code': 0
    })

@app.route('/api/delete_booking', methods=['GET', 'POST'])
def delete_booking():
    username = request.json.get('username')
    roomid = request.json.get('roomid')
    bookdate = request.json.get('bookdate')

    booking = Booking.query.filter_by(username=username, roomid=roomid, bookdate=bookdate).first()
    db.session.delete(booking)
    db.session.commit()

    return jsonify({
        'code': 0
    })

@app.route('/api/upload_file', methods=['POST'])
def upload_file():
    file = request.files['files']
    filename = file.filename
    print(file)
    print(filename)

    reader = csv.reader(codecs.iterdecode(file, 'utf-8'))
    data = list(reader)

    for row in data[1:]:
        room = RoomInfo(row[0], row[1], row[2], row[3])
        db.session.add(room)

    db.session.commit()

    return jsonify({
        'code': 0
    })

@app.route('/api/check_in', methods=['GET', 'POST'])
def check_in():
    username = request.json.get('username')
    roomid = request.json.get('roomid')
    bookdate = request.json.get('bookdate')

    room = RoomInfo.query.filter_by(roomid=roomid).first()

    if room.roomstate == '正在处理':
        return jsonify({
            'code': 1,
            'msg': '房间正在处理，请稍后再试'
        })

    room.roomstate = '已入住'
    room.username = username

    booking = Booking.query.filter_by(username=username, roomid=roomid, bookdate=bookdate).first()
    # print(bookdate)
    # if booking:
    #     print(booking)
    booking.money += 300

    db.session.commit()

    return jsonify({
        'code': 0
    })

@app.route('/api/check_out', methods=['GET', 'POST'])
def check_out():
    username = request.json.get('username')
    roomid = request.json.get('roomid')
    bookdate = request.json.get('bookdate')
    money = request.json.get('money')

    room = RoomInfo.query.filter_by(roomid=roomid).first()
    room.roomstate = '正在处理'
    room.username = ''

    booking = Booking.query.filter_by(username=username, roomid=roomid, bookdate=bookdate).first()
    booking.money -= 300
    booking.money += money
    booking.isActive = '否'

    db.session.commit()

    return jsonify({
        'code': 0
    })

# Change Password
@app.route('/api/change_password', methods=['GET', 'POST'])
def change_password():
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.filter_by(username=username).first()
    user.password = password

    db.session.commit()

    return jsonify({
        'code': 0
    })

@app.route('/api/change_password_by_old_password', methods=['GET', 'POST'])
def change_password_by_old_password():
    username = request.json.get('username')
    old_password = request.json.get('old_password')
    new_password = request.json.get('new_password')

    user = User.query.filter_by(username=username).first()
    if user.password != old_password:
        return jsonify({
            'code': 1,
            'msg': '原密码错误'
        })

    user.password = new_password

    db.session.commit()

    return jsonify({
        'code': 0
    })

@app.route('/api/cancel_booking', methods=['GET', 'POST'])
def cancel_booking():
    username = request.json.get('username')
    roomid = request.json.get('roomid')
    bookdate = request.json.get('bookdate')

    booking = Booking.query.filter_by(username=username, roomid=roomid, bookdate=bookdate).first()
    booking.isActive = '否'

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    msg = ''

    if int(time.mktime(time.strptime(str(booking.todate), "%Y-%m-%d %H:%M:%S"))) - int(time.mktime(time.strptime(now, "%Y-%m-%d %H:%M:%S"))) < 86400:
        msg = '您的预定日期已过期，无法取消预定'

    elif int(time.mktime(time.strptime(booking.fromdate.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S"))) >= int(time.mktime(time.strptime(now, "%Y-%m-%d %H:%M:%S"))):
        db.session.delete(booking)
        # return jsonify({
        #     'code': 0,
        #     'msg': '取消成功，全额退款'
        # })
        msg = '取消成功，全额退款'

    else:
        span = (int(time.mktime(time.strptime(str(booking.todate), "%Y-%m-%d %H:%M:%S"))) - int(time.mktime(time.strptime(now, "%Y-%m-%d %H:%M:%S")))) / 86400
        during = (int(time.mktime(time.strptime(str(booking.todate), "%Y-%m-%d %H:%M:%S"))) - int(time.mktime(time.strptime(str(booking.fromdate), "%Y-%m-%d %H:%M:%S")))) / 86400
        day_price = booking.money / during
        money = day_price * span
        # return jsonify({
        #     'code': 0,
        #     'msg': '取消成功，退款金额为' + str(float("{:.2f}".format(money))) + '元'
        # })
        msg = '取消成功，退款金额为' + str(float("{:.2f}".format(money))) + '元'

    db.session.commit()
    return jsonify({
        'code': 0,
        'msg': msg
    })

@app.route('/api/get_user_list', methods=['GET', 'POST'])
def get_user_list():
    users = User.query.all()
    user_list = []
    for user in users:
        user_list.append(user.to_dict())

    return jsonify({
        'code': 0,
        'data': user_list
    })

# Get user info
@app.route('/api/get_user_info', methods=['GET', 'POST'])
def get_user_info():
    username = request.json.get('username')

    user = User.query.filter_by(username=username).first()

    return jsonify({
        'code': 0,
        'data': user.to_dict()
    })

@app.route('/api/add_user', methods=['GET', 'POST'])
def add_user():
    username = request.json.get('username')
    password = request.json.get('password')
    phone = request.json.get('tele')
    id = request.json.get('id')

    user = User(username=username, password=password, tele=phone, id=id, validationcode='done')

    db.session.add(user)
    db.session.commit()

    return jsonify({
        'code': 0
    })

@app.route('/api/delete_user', methods=['GET', 'POST'])
def delete_user():
    username = request.json.get('username')

    user = User.query.filter_by(username=username).first()
    db.session.delete(user)

    db.session.commit()

    return jsonify({
        'code': 0
    })

# update user
@app.route('/api/update_user', methods=['GET', 'POST'])
def update_user():
    username = request.json.get('username')
    password = request.json.get('password')
    phone = request.json.get('tele')
    id = request.json.get('id')

    user = User.query.filter_by(username=username).first()
    user.password = password
    user.tele = phone
    user.id = id

    db.session.commit()

    return jsonify({
        'code': 0
    })

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=5001)