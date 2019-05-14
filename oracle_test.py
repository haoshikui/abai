# -*- coding: utf8 -*-

import cx_Oracle
import csv
import time
import os
import cx_Oracle
import datetime
# 编码转换
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
#dt = datetime.datetime.now()
M = []
csvfile = open('1.csv', 'r', encoding='UTF-8')
reader = csv.reader(csvfile)


for line in reader:
    try:
        M.append((line[0],line[1],line[2],line[3]))
    except AttributeError:
        pass

csvfile.close()



#创建数据库连接
conn = cx_Oracle.Connection('cge/cge_123@127.0.0.1:1521/orcl')

#获取操作游标
cursor = conn.cursor()
print(len(M))

print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
print('===begin===')

cursor.prepare("INSERT INTO MY_TABLE (ID, COMPANY, DEPARTMENT, NAME) VALUES (:1,:2,:3,:4)")

print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
print('prepare end')

for i in range(1, 31):
    begin = (i - 1) * 30000
    end = i * 30000
    cursor.executemany(None, M[begin:end])
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), '=>', begin, '-', end, '(',  len(M[begin:end]), ')','finish')

print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
print('execute end')

conn.commit()
#885640
print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
print('end')

r = cursor.execute("SELECT COUNT(*) FROM MY_TABLE")
print(cursor.fetchone())

#关闭连接，释放资源
cursor.close()
conn.close()