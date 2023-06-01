import pymysql
from pymysql import *

pymysql.install_as_MySQLdb()


class InitDataBase:
    def __init__(self):
        self.con = connect(host='127.0.0.1', user='root', passwd='mengsong', port=3306, db='apis', charset='utf8')
        self.cursor = self.con.cursor(cursor=pymysql.cursors.DictCursor)


class Water(InitDataBase):
    def get_all_water_use(self):
        cur = self.cursor
        cur.execute("select * from water_use")
        data = cur.fetchall()
        return data

    def get_water_amount(self):
        cur = self.cursor
        cur.execute("select date,value from water_amount order by date")
        data = cur.fetchall()
        return data


class Population(InitDataBase):
    def get_production_average(self):
        cur = self.cursor
        cur.execute("select year,average,index_number from production_average")
        data = cur.fetchall()
        return data

    def get_permanent(self):
        cur = self.cursor
        cur.execute("select * from permanent_population")
        data = cur.fetchall()
        return data

    def get_production_total(self):
        cur = self.cursor
        cur.execute("select * from production_total")
        data = cur.fetchall()
        return data

    def get_job(self):
        cur = self.cursor
        cur.execute("select * from job")
        data = cur.fetchall()
        return data

    def get_pay_index(self):
        cur = self.cursor
        cur.execute("select * from pay_index")
        data = cur.fetchall()
        return data

    def get_pay_level(self):
        cur = self.cursor
        cur.execute("select * from pay_level")
        data = cur.fetchall()
        return data


class Tree(InitDataBase):
    def forest(self):
        cur = self.cursor
        cur.execute("select year,cover,area from forest order by year")
        data = cur.fetchall()
        return data


class DataCenter(InitDataBase):

    def get_pollution_company_list(self):
        cur = self.cursor
        cur.execute("select id, company_name from pollution_company")
        data = cur.fetchall()
        return data

    def get_pollution_sources(self, company_name):
        cur = self.cursor
        base_sql = "select pollution_sources.*,pollution_company.company_name  from pollution_sources join " \
                   "pollution_company on pollution_sources.company_id = pollution_company.id where " \
                   "pollution_company.company_name = '{}'".format(company_name)

        cur.execute(base_sql + "and pollutant='COD'")
        cod_data = cur.fetchall()
        cur = self.cursor
        base_sql = "select pollution_sources.*,pollution_company.company_name  from pollution_sources join " \
                   "pollution_company on pollution_sources.company_id = pollution_company.id where " \
                   "pollution_company.company_name = '{}'".format(company_name)

        cur.execute(base_sql + "and pollutant='氨氮'")
        ad_data = cur.fetchall()
        return {'cod_data': cod_data, 'ad_data': ad_data}

    def get_industrial(self):
        cur = self.cursor
        cur.execute("select year, total, light, heavy from industrial")
        return cur.fetchall()

    def get_contraceptives(self):
        cur = self.cursor
        cur.execute("select name, phone, leader, state from contraceptives limit 50")
        return cur.fetchall()

    def get_contraceptives_detail(self):
        cur = self.cursor
        cur.execute("select * from contraceptives")
        return cur.fetchall()

    def get_people(self):
        cur = self.cursor
        cur.execute("select * from people")
        return cur.fetchall()

    def get_income(self):
        cur = self.cursor
        cur.execute("select salary,tend,property,transfer  from income")
        return cur.fetchall()

    def get_pay(self):
        cur = self.cursor
        cur.execute("select * from pay")
        return cur.fetchall()


class User(InitDataBase):
    """连接数据库"""

    def login(self, username, password):
        """查询某条数据"""
        cur = self.con.cursor()
        cur.execute("select username, password, id from user where username='{}' union select username, password, "
                    "id from user where phone_number='{}'".format(username, username))
        data = cur.fetchall()
        if len(data) == 0:
            return False
        pwd = data[0][0]
        if pwd != password:
            return False
        return data[0][2]

    def set_token(self, username, token):
        cur = self.con.cursor()
        cur.execute("update user set token='{}' where username='{}'".format(token, username))
        self.con.commit()

    def get_all_user(self):
        cur = self.cursor
        cur.execute("select id, username from user")
        return cur.fetchall()

    def get_all_user_part(self):
        cur = self.cursor
        cur.execute("select id, username, real_name, nick_name from user")
        return cur.fetchall()

    def get_user_detail(self, user_id):
        cur = self.cursor
        cur.execute("select * from user where id='{}'".format(user_id))
        return cur.fetchall()

    def add_user(self, real_name, nick_name, email, sex, phone_number, password, role, username):
        cur = self.cursor
        result = cur.execute(
            "insert into user (real_name, nick_name, email, sex, phone_number, password, role, username) values('{}', "
            "'{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(real_name, nick_name, email, sex, phone_number, password,
                                                               role, username))
        self.con.commit()
        return result

    def update_user(self, id, real_name, nick_name, email, sex, phone_number, password, role, username):
        cur = self.cursor
        result = cur.execute(
            "update user set real_name='{}', nick_name='{}', email='{}', sex='{}', phone_number='{}', password='{}', "
            "role='{}', username='{}' where id='{}'".format(real_name, nick_name, email, sex, phone_number,
                                                            password, role, username, id))
        self.con.commit()
        return result

    def delete_user(self, id):
        cur = self.cursor
        result = cur.execute("delete from user where id='{}'".format(id))
        self.con.commit()
        return result

    def get_routes(self, userId):
        cur = self.cursor
        cur.execute("select permission.permission_name, permission.permission_path from role_user inner join "
                    "role_permission on role_user.role_id = role_permission.role_id inner join permission on "
                    "role_permission.permission_id = permission.id where role_user.user_id = '{}' group by "
                    "permission.permission_name, permission.permission_path".format(userId))
        return cur.fetchall()


class Role(InitDataBase):
    def add_role(self, role_name):
        cur = self.cursor
        result = cur.execute("insert into role (role_name) values('{}')".format(role_name))
        self.con.commit()
        return result

    def get_role_list(self):
        cur = self.cursor
        cur.execute("select id, role_name from role")
        return cur.fetchall()

    def update_role(self, id, role_name):
        cur = self.cursor
        result = cur.execute("update role set role_name='{}' where id='{}'".format(role_name, id))
        self.con.commit()
        return result

    def delete_role(self, id):
        cur = self.cursor
        result = cur.execute("delete from role where id='{}'".format(id))
        self.con.commit()
        return result


class Permission(InitDataBase):
    def add_permission(self, permission_name, permission_path):
        cur = self.cursor
        result = cur.execute("insert into permission (permission_name, permission_path) values('{}', '{}')".format(permission_name, permission_path))
        self.con.commit()
        return result

    def get_permission_list(self):
        cur = self.cursor
        cur.execute("select id, permission_name, permission_path from permission")
        return cur.fetchall()

    def update_permission(self, id, permission_name, permission_path):
        cur = self.cursor
        result = cur.execute("update permission set permission_name='{}', permission_path='{}' where id='{}'".format(permission_name, permission_path, id))
        self.con.commit()
        return result

    def delete_permission(self, id):
        cur = self.cursor
        result = cur.execute("delete from permission where id='{}'".format(id))
        self.con.commit()
        return result


class RolePermission(InitDataBase):
    def bind_role_permission(self, role_id, permission_list):
        cur = self.cursor
        values = []
        for permission_id in permission_list:
            values.append("({}, {})".format(role_id, permission_id))
        values_str = ', '.join(values)
        cur.execute("delete from role_permission where role_id='{}'".format(role_id))
        cur.execute("insert into role_permission (role_id, permission_id) values {}".format(values_str))
        self.con.commit()
        return

    def get_role_permission(self, role_id):
        cur = self.cursor
        cur.execute("select permission_id from role_permission where role_id='{}'".format(role_id))
        data = cur.fetchall()
        return data


class RoleUser(InitDataBase):
    def bind_role_user(self, role_id, user_list):
        cur = self.cursor
        values = []
        for user_id in user_list:
            values.append("({}, {})".format(role_id, user_id))
        values_str = ', '.join(values)
        cur.execute("delete from role_user where role_id='{}'".format(role_id))
        cur.execute("insert into role_user (role_id, user_id) values {}".format(values_str))
        self.con.commit()
        return

    def get_role_user(self, role_id):
        cur = self.cursor
        cur.execute("select user_id from role_user where role_id='{}'".format(role_id))
        data = cur.fetchall()
        return data


class UserPermission(InitDataBase):
    def get_user_permission(self, user_id):
        cur = self.cursor
        cur.execute("select role_id from role_user where user_id='{}'".format(user_id))
        role_id_list = cur.fetchall()
        new_role_id_list = []
        for role in role_id_list:
            new_role_id_list.append("'" + str(role['role_id']) + "'")
        role_id_list_str = '({})'.format(', '.join(new_role_id_list))
        sql = "select permission_id from role_permission where role_id in {}".format(role_id_list_str)
        cur.execute(sql)
        permission_id_list = cur.fetchall()
        new_permission_id_list = []
        for role in permission_id_list:
            new_permission_id_list.append("'" + str(role['permission_id']) + "'")
        permission_id_list_str = '({})'.format(', '.join(new_permission_id_list))
        sql = "select id, permission_name from permission where id in {}".format(permission_id_list_str)
        print(sql)
        cur.execute(sql)
        return cur.fetchall()
