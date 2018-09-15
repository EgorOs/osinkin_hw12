#!/usr/bin/env python3

import psycopg2
import gzip
import csv

conn = psycopg2.connect(host='localhost', port='5431', user='root', password='password', dbname='homework')
cursor = conn.cursor()
# sql =   """
#         CREATE TABLE city (
#         city_id SERIAL NOT NULL PRIMARY KEY,
#         city_name VARCHAR(255) NOT NULL UNIQUE
#         );
#         """
# cursor.execute(sql)
# conn.commit()
bosses_ids = sorted({r.split(',')[-2] for r in gzip.open('csv/EMPLOYEE.csv.gz', mode='rt')})
print(len(bosses_ids))


with open('csv/DEPTS.csv', mode='rt') as f:
    # skip header line
    next(f)
    ctr = 1
    dep_2_id = {}
    for row in f:
        dep, city = row.split(',')
        sql = """INSERT INTO department(department_id, department_name, department_city) VALUES (%s, '%s', '%s');"""%(ctr, dep, city)
        dep_2_id[dep] = ctr
        cursor.execute(sql)
        conn.commit()
        ctr += 1



with gzip.open('csv/EMPLOYEE.csv.gz', mode='rt') as f:
    # get first row
    em_id, fn, ln, depart, city, boss, salary = next(f).split(',')
    sql_insert = """INSERT INTO employee(employee_id, first_name, last_name, employee_department, employee_city, boss, salary) VALUES """
    sql_values = ''
    ctr = 1
    for row in f:
        em_id, fn, ln, dep, city, boss, salary = row.split(',')
        # print('here')
        if em_id in bosses_ids:
            sql_values += """(%s, '%s', '%s', %s, '%s', %s, %s)"""%(em_id, fn, ln, dep_2_id[dep], city, em_id, salary)
            if ctr % 500 == 0:
                cursor.execute(sql_insert + sql_values)
                conn.commit()
                sql_values = ''
                print(500)
            else:
                sql_values += ',' 
        ctr += 1     
        # print(sql_insert, sql_values)
    cursor.execute(sql_insert + sql_values)
    conn.commit()
    print('ok')


conn.close()

# wierd stuff in database
# Not none check
# salary - ok
# 106014 - No boss
# city - ok
# department - ok
# last_name - ok
# name - ok
# id - ok
# insert into employee values(12, 'mr','employee', 123, null, 111, 1337)
# insert into employee values(14, 'mr','another', 123, 12, 111, 'city')