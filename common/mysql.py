# -*- coding: utf-8 -*-
# Powered By: ECHO
# @Time : 2020/12/13 19:24
import pymysql

from common import config
from common.logger import logger


class Mysql:
    def __init__(self):
        # 配置mysql参数
        self.mysql_config = {
            'mysqluser': "root",
            'mysqlpassword': "123456",
            'mysqlport': 3306,
            'mysqlhost': 'localhost',
            'mysqldb': 'test_project',
            'mysqlcharset': "utf8"
        }
        # 从配置文件读取配置
        for key in self.mysql_config:
            try:
                self.mysql_config[key] = config.config[key]
            except Exception as e:
                logger.exception(e)
        # 把端口处理为整数
        try:
            self.mysql_config['mysqlport'] = int(self.mysql_config['mysqlport'])
        except Exception as e:
            logger.exception(e)

    # 处理.sql备份文件为SQL语句
    def __read_sql_file(self,file_path):
        # 打开SQL文件到f
        sql_list = []
        with open(file_path, 'r', encoding='utf8') as f:
            # 逐行读取和处理SQL文件
            for line in f.readlines():
                # 如果是配置数据库的SQL语句，就去掉末尾的换行
                if line.startswith('SET'):
                    sql_list.append(line.replace('\n', ''))
                # 如果是删除表的语句，则改成删除表中的数据
                elif line.startswith('DROP'):
                    sql_list.append(line.replace('DROP', 'TRUNCATE').replace(' IF EXISTS', '').replace('\n', ''))
                # 如果是插入语句，也删除末尾的换行
                elif line.startswith('INSERT'):
                    sql_list.append(line.replace('\n', ''))
                elif line.startswith('delete'):
                    sql_list.append(line.replace('\n', ''))
                # 如果是其他语句，就忽略
                else:
                    pass
        return sql_list


    # 初始化mysql配置
    def init_mysql(self,path):
        # 创建连接，执行语句的时候是在这个连接
        connect = pymysql.connect(
            user=self.mysql_config['mysqluser'],
            password=self.mysql_config['mysqlpassword'],
            port=self.mysql_config['mysqlport'],
            host=self.mysql_config['mysqlhost'],
            db=self.mysql_config['mysqldb'],
            charset=self.mysql_config['mysqlcharset']
        )

        # 获取游标
        cursor = connect.cursor()
        logger.info("正在恢复%s数据库" % path)
        # 一行一行执行SQL语句
        for sql in self.__read_sql_file(path):
            cursor.execute(sql)
            connect.commit()
        # 关闭游标和连接
        cursor.close()
        connect.close()

    def select_mysql(self,sql):
        connect = pymysql.connect(
            user=self.mysql_config['mysqluser'],
            password=self.mysql_config['mysqlpassword'],
            port=self.mysql_config['mysqlport'],
            host=self.mysql_config['mysqlhost'],
            db=self.mysql_config['mysqldb'],
            charset=self.mysql_config['mysqlcharset']
        )
        #创建游标
        cursor = connect.cursor()
        cursor.execute(sql)
        connect.commit()
        # 使用fetchall()获取全部数据 元组
        res = cursor.fetchall()
        cursor.close()
        connect.close()
        return res



# 调试代码
if __name__ == '__main__':
    config.get_config('../lib/conf/conf.properties')
    # logger.info(config.config)
    mysql = Mysql()
    # mysql.init_mysql('../lib/conf/userinfo.sql')
    res = mysql.select_mysql('select * from userinfo;')
    print(list(res)[1][4])
    print(type(list(res)))
