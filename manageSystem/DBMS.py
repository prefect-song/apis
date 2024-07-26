import pymysql
from pymysql import *

pymysql.install_as_MySQLdb()


class InitDataBase:
    def __init__(self):
        self.con = connect(host='127.0.0.1', user='root', passwd='mengsong', port=3306, db='file_manage', charset='utf8')
        self.cursor = self.con.cursor(cursor=pymysql.cursors.DictCursor)


class Permission(InitDataBase):
    def insert_permission(self, user_id):
        cur = self.cursor
        result = cur.execute("insert into permission (user_id, is_deletable) values('{}', '0')".format(user_id))
        self.con.commit()
        return result

    def update_permission(self, is_deletable, user_id):
        cur = self.cursor
        result = cur.execute("update permission set is_deletable='{}' where user_id='{}'".format(is_deletable, user_id))
        self.con.commit()
        return result

    def get_permission(self, user_id):
        cur = self.cursor
        cur.execute("select is_deletable from permission where user_id='{}'".format(user_id))
        return cur.fetchall()


class User(InitDataBase):
    def register(self, username, password, create_time):
        cur = self.cursor
        result = cur.execute("insert into users (username, password, create_time, last_logintime) values('{}', '{}', '{}', '{}')".format(username, password, create_time, create_time))
        self.con.commit()
        cur = self.cursor
        cur.execute("select id from users where username='{}' and password='{}'".format(username, password))
        user_id = cur.fetchall()[0]["id"]
        Permission().insert_permission(user_id)
        return result

    def login(self, username, password):
        cur = self.con.cursor()
        cur.execute("select username, password, id from users where username='{}'".format(username))
        data = cur.fetchall()
        if len(data) == 0:
            return False
        pwd = data[0][0]
        if pwd != password:
            return False
        return data[0][2]

    def set_token(self, username, token):
        cur = self.con.cursor()
        cur.execute("update users set token='{}' where username='{}'".format(token, username))
        self.con.commit()

    def verify_token(self, user_id):
        cur = self.con.cursor()
        cur.execute("select token, avatar, username, is_superuser from users where id='{}'".format(user_id))
        return cur.fetchall()

    def get_user_info(self, token):
        cur = self.con.cursor()
        cur.execute("select id, username, password, phone, last_logintime from users where token='{}'".format(token))
        return cur.fetchall()[0]

    def update_user_info(self, username, password, phone, update_time, id):
        cur = self.cursor
        result = cur.execute(
            "update users set username='{}', password='{}', phone='{}', update_time='{}' where id='{}'"
            .format(username, password, phone, update_time, id))
        self.con.commit()
        return result

    def update_user_last_logintime(self, last_logintime, token):
        cur = self.con.cursor()
        result = cur.execute("update users set last_logintime='{}' where token='{}'".format(last_logintime, token))
        self.con.commit()
        return result


class SuperUser(InitDataBase):
    def super_get_user_info(self):
        cur = self.cursor
        cur.execute("select u.id, u.username, u.password, u.phone, u.last_logintime, u.create_time, p.is_deletable from users u join permission p on u.id = p.user_id")
        return cur.fetchall()


class File(InitDataBase):
    def upload_file(self, filename, path, size, create_time, user_id):
        cur = self.cursor
        result = cur.execute("insert into filerecord (filename, path, size, create_time, user_id) "
                             "values('{}', '{}', '{}', '{}', '{}')".format(filename, path, size, create_time, user_id))
        self.con.commit()
        self.user_operate_record(user_id, filename, create_time, "上传")
        return result

    def get_filepath_by_fileid(self, fileid):
        cur = self.cursor
        cur.execute("select path from filerecord where id='{}'".format(fileid))
        return cur.fetchall()

    def get_file(self, user_id, filename, is_deleted):
        # 管理员可以获取所有文件列表
        if user_id == '2':
            cur = self.cursor
            cur.execute(
                "SELECT f.id, f.filename, f.size, f.create_time, f.path, f.user_id, u.username FROM filerecord f join users "
                "u on f.user_id = u.id  where f.is_deleted='{}' and f.filename LIKE '%{}%'".format(is_deleted, filename))
            return cur.fetchall()
        else:
            is_deletable_permission = Permission().get_permission(user_id)[0]["is_deletable"]
            if is_deletable_permission:
                cur = self.cursor
                cur.execute("SELECT f.id, f.filename, f.size, f.create_time, f.path, f.user_id, u.username FROM filerecord f join users "
                            "u on f.user_id = u.id  where (f.user_id='{}' or f.user_id='2') and f.is_deleted='{}' and f.filename LIKE '%{}%'".format(user_id, is_deleted, filename))
                return cur.fetchall()
            # 没有删除管理员文件的权限时
            else:
                if is_deleted:
                    cur = self.cursor
                    cur.execute(
                        "SELECT f.id, f.filename, f.size, f.create_time, f.path, f.user_id, u.username FROM filerecord f join users "
                        "u on f.user_id = u.id  where f.user_id='{}' and f.is_deleted='{}' and f.filename LIKE '%{}%'".format(
                            user_id, is_deleted, filename))
                    return cur.fetchall()
                else:
                    cur = self.cursor
                    cur.execute(
                        "SELECT f.id, f.filename, f.size, f.create_time, f.path, f.user_id, u.username FROM filerecord f join users "
                        "u on f.user_id = u.id  where (f.user_id='{}' or f.user_id='2') and f.is_deleted='{}' and f.filename LIKE '%{}%'".format(
                            user_id, is_deleted, filename))
                    return cur.fetchall()

    def recycle_file(self, id):
        cur = self.cursor
        result = cur.execute(
            "update filerecord set is_deleted='1' where id='{}'".format(id))
        self.con.commit()
        return result

    def recovery_file(self, id):
        cur = self.cursor
        result = cur.execute(
            "update filerecord set is_deleted='0' where id='{}'".format(id))
        self.con.commit()
        return result

    def delete_file(self, id, user_id, filename, delete_time):
        cur = self.cursor
        result = cur.execute("delete from filerecord where id='{}'".format(id))
        self.con.commit()
        self.user_operate_record(user_id, filename, delete_time, "删除")
        return result

    def user_operate_record(self, user_id, filename, time, type):
        cur = self.cursor
        cur.execute("insert into user_operate_record (user_id, filename, time, type) values('{}', '{}', '{}', '{}')"
                    .format(user_id, filename, time, type))
        self.con.commit()

    def get_operate_record(self, user_id):
        if user_id == '2':
            cur = self.cursor
            cur.execute("select u.username, r.filename, r.time, r.type from user_operate_record r join users u on "
                        "r.user_id = u.id")
            return cur.fetchall()
        else:
            cur = self.cursor
            cur.execute("select u.username, r.filename, r.time, r.type from user_operate_record r join users u on "
                        "r.user_id = u.id where r.user_id='{}'".format(user_id))
            return cur.fetchall()
