from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DatabaseManagement():
    def conn(self):
        self.engine = create_engine('',echo=True)  # 初始化数据库连接
        DBsession = sessionmaker(bind=self.engine)  # 创建DBsession类
        self.session = DBsession()  # 创建对象

    def create_session(self):  # 创建session
        DBsession = sessionmaker(bind=self.engine)  # 创建DBsession类
        self.session = DBsession()  # 创建对象

    def add_obj(self, obj):  # 添加内容
        self.session.add(obj)
        self.session.commit()  # 提交
        return obj

    def query_all(self, target_class, query_filter):  # 查询内容
        result_list = self.session.query(target_class).filter(query_filter).all()
        return result_list

    def update_by_filter(self, obj, update_hash, query_filter):  # 更新内容
        self.session.query(obj.__class__).filter(query_filter).update(update_hash)
        self.session.commit()

    def delete_by_filter(self, obj, query_filter):  # 删除内容
        self.session.query(obj).filter(query_filter).delete()

    def close(self):  # 关闭session
        self.session.close()

    def execute_sql(self, sql_str):  # 执行sql语句
        return self.session.execute(sql_str)