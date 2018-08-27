# coding=utf-8


'''
发生崩溃把时间、机型、堆栈信息记录到crash的数据库表中
方便后续统计和排查

@author xinxi
'''

import time
import datetime
import pymysql
from SQLConfig import *
import logger

data = None
sql = None


class CrashSQL():
    def __init__(self):
        self.localhost = localhost
        self.port = port
        self.user = user
        self.pwd = pwd
        self.db = db
        self.tablename = tablename

    def connectmysql(self, sql):
        '''
        连接数据库方法
        :param sql:sql语句
        :return:
        '''
        global data
        try:
            # 创建连接
            conn = pymysql.connect(host=self.localhost, port=self.port, user=self.user, passwd=self.pwd, db=self.db,
                                   charset='utf8')
            # 创建游标
            cursor = conn.cursor()
            # 执行SQL，并返回收影响行数
            cursor.execute(sql)
            # 返回所有数据
            data = cursor.fetchall()
            # 关闭游标
            cursor.close()
            # 关闭连接
            conn.close()
        except Exception, e:
            logger.log_error("连接数据异常:" + str(e))
            data = None

        finally:
            return data

    def selectcrash(self, condition):
        '''
        查询crash的方法
        :param condition: 查询条件
        :return:
        '''
        global sql
        try:
            sql = "SELECT %s FROM %s " % (condition, self.tablename)
            logger.log_info('查询%s语句:%s' % (self.tablename, sql))
            print self.connectmysql(sql)

        except Exception as e:
            logger.log_error('查询%s语句:%s,失败原因:%s' % (self.tablename, sql, str(e)))

    def select_table(self, tablename, wheresql='', selectsql='*'):
        '''
        查询数据库通用函数
        :param tablename: 查询的表名,字符串形式
        :param wheresql: 查询条件字符串，sql语句中WHERE wheresql
        :param selectsql: 要查询的内容,字符串形式，sql语句中SELECT selectsql,默认*查询全部字段
        :return: 返回一个查询结果集（tuple）
        '''
        try:
            con = pymysql.connect(
                host=self.localhost,
                port=self.port,
                user=self.user,
                passwd=self.pwd,
                db=self.db,
                charset="utf8",
            )
            curs = con.cursor()
            if wheresql == '':
                sql_select = """
                                    SELECT %s FROM %s""" % \
                             (selectsql, tablename)
            else:
                sql_select = """
                            SELECT %s FROM %s WHERE %s""" % \
                             (selectsql, tablename, wheresql)
            # print 'sql_select is ' +  sql_select
            try:
                print sql_select
                curs.execute(sql_select)
                select_result = curs.fetchall()
            finally:
                curs.close()
                con.close()
            return select_result
        except pymysql.Error, e:
            print "执行数据表查询异常：", e

    def insert_table(self, valuesql):
        '''
        向指定数据表中插入数据
        :param tablename: 被插入表名
        :param valuesql: 插入的值，字符串形式，sql语句中VALUES(valuesql),参数fieldsql有值时，与之对应
        :param fieldsql: 被插入的字段，字符串形式，sql语句中tablename(fieldsql),默认为空
        :return: 返回插入结果
        :exception mysql异常操作存在mysql.log中
        '''
        try:
            insert_result = ''

            con = pymysql.connect(
                host=self.localhost,
                port=self.port,
                user=self.user,
                passwd=self.pwd,
                db=self.db,
                charset="utf8",
            )
            curs = con.cursor()

            # 插入时间
            sql_insert = """INSERT INTO %s (%s) VALUES(%s)""" % \
                         (self.tablename, """create_time,device_name,apk_version,issue,crash_detail""", valuesql)

            logger.log_info('插入的sql语句是:' + sql_insert)

            try:
                insert_result = curs.execute(sql_insert)
            except pymysql.Error, e:
                logger.log_error("执行数据异常!!!" + str(e))

            finally:
                curs.close()
                con.commit()
                con.close()
            return insert_result
        except pymysql.Error, e:
            logger.log_error("执行数据异常!!!" + str(e))

