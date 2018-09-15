#!/usr/bin/env python3

import psycopg2
import gzip
import csv


def load_deps(dest: str, connection_params: dict) -> dict:
    """Fills the department table"""
    with psycopg2.connect(**connection_params) as conn, open(dest, mode='rt') as f:
        cursor = conn.cursor()
        idx = 1
        dep_2_id = {}
        # skip header line
        next(f)
        for row in f:
            dep, city = row.split(',')
            sql = """INSERT INTO department(department_id, department_name, department_city) VALUES (%s, '%s', '%s');"""%(idx, dep, city)
            dep_2_id[dep] = idx
            cursor.execute(sql)
            conn.commit()
            idx += 1
    return dep_2_id


def load_employees(dest: str, nchunks: int, connection_params: dict, dep_2_id: dict):
    """Fills the employee table, nchunks parameter defines the number of chunks
    employees will be separated into, thus the number of SQL queries"""
    with psycopg2.connect(**connection_params) as conn, gzip.open(dest, mode='rt') as f:
        cursor = conn.cursor()

        # Load bosses first to avoid crushes on loading subordinates
        bosses_ids = set()

        sql_common = """INSERT INTO employee(employee_id, first_name, last_name, employee_department, employee_city, boss, salary) VALUES """
        sql_values = ''
        next(f)
        n_subordinates = 0
        for row in f:
            em_id, fn, ln, dep, city, boss_id, salary = row.split(',')
            if em_id == boss_id or boss_id == '':
                sql_values += """, (%s, '%s', '%s', %s, '%s', %s, %s)"""%(em_id, fn, ln, dep_2_id[dep], city, em_id, salary)
                bosses_ids.add(em_id)
            else:
                n_subordinates += 1

        # remove extra comma
        sql = sql_common + sql_values[1::]
        cursor.execute(sql)
        conn.commit()

    with psycopg2.connect(**connection_params) as conn, gzip.open(dest, mode='rt') as f:
        cursor = conn.cursor()
        # Separate subordinates in chunks and load them
        chunk_size = n_subordinates // nchunks
        current_chunk_size = 0
        sql_common = """INSERT INTO employee(employee_id, first_name, last_name, employee_department, employee_city, boss, salary) VALUES """
        sql_values = ''
        next(f)
        for row in f:
            em_id, fn, ln, dep, city, boss_id, salary = row.split(',')
            if current_chunk_size < chunk_size:
                if em_id not in bosses_ids:
                    sql_values += """, (%s, '%s', '%s', %s, '%s', %s, %s)"""%(em_id, fn, ln, dep_2_id[dep], city, em_id, salary)
                    current_chunk_size += 1
            else:
                sql = sql_common + sql_values[1::]
                cursor.execute(sql)
                conn.commit()
                sql_values = """, (%s, '%s', '%s', %s, '%s', %s, %s)"""%(em_id, fn, ln, dep_2_id[dep], city, em_id, salary)
                current_chunk_size = 1
                print('chunk processed')

        # Commit last unfilled chunk if it exists
        if current_chunk_size != 0:
            sql = sql_common + sql_values[1::]
            cursor.execute(sql)
            conn.commit()


#903,160
#903196 - true val

connection_params = {
    'host':'localhost', 
    'port':'5431', 
    'user':'root', 
    'password':'password', 
    'dbname':'homework'
}

dep_2_id = load_deps('csv/DEPTS.csv', connection_params)
load_employees('csv/EMPLOYEE.csv.gz', 5, connection_params, dep_2_id)

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