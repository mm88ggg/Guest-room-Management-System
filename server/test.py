from dbutil import DatabaseManagement
from room import RoomState, RoomInfo
from user import User
from sqlalchemy import and_

import _thread
import time

class Test():
    def __init__(self):
        self.db_obj = DatabaseManagement()

    def process(self):
        user_list = User.query.all()
        print(user_list)

def run():
    time.sleep(5)
    print('asdf')

if __name__ == '__main__':
    test = Test()
    test.process()
    test.process()
    test.process()
    test.process()
    test.process()
