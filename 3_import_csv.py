#!/usr/bin/env python3

import psycopg2
import gzip
import csv
from time import time


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
            sql = """
            INSERT INTO department(department_id, department_name, 
            department_city) VALUES (%s, '%s', '%s');"""%(idx, dep, city)
            dep_2_id[dep] = idx
            cursor.execute(sql)
            conn.commit()
            idx += 1
    return dep_2_id


def load_employees(dest: str, chunk_size: int, connection_params: dict, dep_2_id: dict):
    """Fills the employee table, chunk_size parameter defines the number of 
    employee records loaded per query"""
    with psycopg2.connect(**connection_params) as conn, gzip.open(dest, mode='rt') as f:
        cursor = conn.cursor()

        # Load bosses first to avoid crushes on loading subordinates
        bosses_ids = set()
        current_chunk_size = 0
        sql_common = """
        INSERT INTO employee(employee_id, first_name, last_name, 
        employee_department, employee_city, boss, salary) VALUES """
        sql_values = ''
        next(f)
        n_subordinates = 0
        loaded_records = 0
        for row in f:
            em_id, fn, ln, dep, city, boss_id, salary = row.split(',')
            if em_id == boss_id or boss_id == '':
                sql_values += """, (%s, '%s', '%s', %s, '%s', %s, %s)""" % (
                    em_id, fn, ln, dep_2_id[dep], city, em_id, salary)
                current_chunk_size += 1
                bosses_ids.add(em_id)
            else:
                n_subordinates += 1

            if current_chunk_size >= chunk_size:
                # remove extra comma from sql_values
                sql = sql_common + sql_values[1::]
                cursor.execute(sql)
                conn.commit()
                loaded_records += current_chunk_size
                print('Loaded %s bosses' % loaded_records)
                current_chunk_size = 0
                sql_values = ''

        if current_chunk_size != 0:
            sql = sql_common + sql_values[1::]
            cursor.execute(sql)
            conn.commit()
            loaded_records += current_chunk_size
            print('Loaded %s bosses' % loaded_records)

        total_records = n_subordinates + len(list(bosses_ids))

    with psycopg2.connect(**connection_params) as conn, gzip.open(dest, mode='rt') as f:
        cursor = conn.cursor()
        # Separate subordinates in chunks and load them
        current_chunk_size = 0
        sql_common = """
        INSERT INTO employee(employee_id, first_name, last_name, 
        employee_department, employee_city, boss, salary) VALUES """
        sql_values = ''
        next(f)
        for row in f:
            em_id, fn, ln, dep, city, boss_id, salary = row.split(',')
            if em_id not in bosses_ids:
                sql_values += """, (%s, '%s', '%s', %s, '%s', %s, %s)""" % (
                    em_id, fn, ln, dep_2_id[dep], city, em_id, salary)
                current_chunk_size += 1

            if current_chunk_size >= chunk_size:
                sql = sql_common + sql_values[1::]
                cursor.execute(sql)
                conn.commit()
                loaded_records += current_chunk_size
                print('Loaded %s / %s employees' % (loaded_records, total_records))
                current_chunk_size = 0
                sql_values = ''

        # Commit last unfilled chunk if it exists
        if current_chunk_size != 0:
            sql = sql_common + sql_values[1::]
            cursor.execute(sql)
            conn.commit()
            loaded_records += current_chunk_size
            print('Loaded %s / %s employees' % (loaded_records, total_records))


connection_params = {
    'host': 'localhost',
    'port': '5431',
    'user': 'root',
    'password': 'password',
    'dbname': 'homework'
}

dep_2_id = load_deps('csv/DEPTS.csv', connection_params)
# load_employees('csv/EMPLOYEE.csv.gz', 200000, connection_params, dep_2_id)


# https://www.dataquest.io/blog/loading-data-into-postgres/
# https://stackoverflow.com/questions/30050097/copy-data-from-csv-to-postgresql-using-python
with psycopg2.connect(**connection_params) as conn, gzip.open('csv/EMPLOYEE.csv.gz', mode='rt') as f:
    cursor = conn.cursor()
    cursor.execute("""
CREATE TABLE test(
    id integer PRIMARY KEY,
    fname varchar,
    lname varchar,
    emp_dep text,
    emp_city varchar,
    boss text,
    salary integer
)
""")

    conn.commit()
    next(f)
    cursor.copy_from(f, 'test', sep=',')
    conn.commit()

    sql = """
UPDATE test
set boss = case when boss = '' then cast(id as text) else boss end
where boss = '' """
    t_start = time()
    cursor.execute(sql)
    conn.commit()
    print('Filled missing values in: %s sec' %(time()-t_start))

    sql = """
UPDATE test
set emp_dep = (select department_id from department where emp_dep = department.department_name)"""
    t_start = time()
    cursor.execute(sql)
    conn.commit()
    print('Numbered departments in: %s sec' %(time()-t_start))

    sql = """
INSERT into employee(employee_id, first_name, last_name, employee_department, boss, salary, employee_city)
select id, fname, lname, cast(emp_dep as integer), cast(boss as integer) as boss, salary, emp_city
from test
where id in (select cast(boss as integer) from test)"""
    t_start = time()
    cursor.execute(sql)
    conn.commit()
    print('Inserted bosses in: %s sec' %(time()-t_start))

    sql = """
    DELETE
from test
where id in (select cast(boss as integer) from test)"""
    t_start = time()
    cursor.execute(sql)
    conn.commit()
    print('Removed bosses from pool in: %s sec' %(time()-t_start))

    sql = """
INSERT into employee(employee_id, first_name, last_name, employee_department, boss, salary, employee_city)
SELECT id, fname, lname, cast(emp_dep as integer), cast(boss as integer) as boss, salary, emp_city
from test
"""
    t_start = time()
    cursor.execute(sql)
    conn.commit()
    print('Inserted the rest of employees: %s sec' %(time()-t_start))