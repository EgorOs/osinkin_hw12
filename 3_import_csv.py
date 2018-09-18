#!/usr/bin/env python3

import psycopg2
import gzip
import csv
from time import time
import os


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


def create_temp_csv(from_dest, name, dep_2_id):

    bosses_ids = {row.split(',')[-2] for row in gzip.open(from_dest, mode='rt')} - {'boss', ''}
    bosses_added = set()
    with gzip.open(from_dest, mode='rt') as f, open(name, mode='w', newline='') as f_out:

        # Load bosses first to avoid crushes on loading subordinates
        next(f)
        writer = csv.writer(f_out, delimiter=',')
        for row in f:
            em_id, fn, ln, dep, city, boss_id, salary = row.split(',')
            if em_id == boss_id and boss_id != '':
                writer.writerow([em_id, fn, ln, dep_2_id[dep],
                                 int(boss_id), int(salary), city])
                bosses_added.add(em_id)
            elif boss_id == '':
                writer.writerow([em_id, fn, ln, dep_2_id[dep],
                                 int(em_id), int(salary), city])
                bosses_added.add(em_id)

    with gzip.open(from_dest, mode='rt') as f, open(name, mode='a', newline='') as f_out:

        bosses_req = bosses_ids - bosses_added
        next(f)
        writer = csv.writer(f_out, delimiter=',')
        for row in f:
            em_id, fn, ln, dep, city, boss_id, salary = row.split(',')
            if em_id in bosses_req:
                writer.writerow([em_id, fn, ln, dep_2_id[dep],
                                 int(boss_id), int(salary), city])

    with gzip.open(from_dest, mode='rt') as f, open(name, mode='a', newline='') as f_out:

        next(f)
        writer = csv.writer(f_out, delimiter=',')
        for row in f:
            em_id, fn, ln, dep, city, boss_id, salary = row.split(',')
            if em_id not in bosses_ids and boss_id != '':
                writer.writerow([em_id, fn, ln, dep_2_id[dep],
                                 int(boss_id), int(salary), city])


connection_params = {
    'host': 'localhost',
    'port': '5431',
    'user': 'root',
    'password': 'password',
    'dbname': 'homework'
}

init_time = time()
dep_2_id = load_deps('csv/DEPTS.csv', connection_params)
temp_csv_name = 'tmp.csv'

create_temp_csv('csv/EMPLOYEE.csv.gz', temp_csv_name, dep_2_id)

with psycopg2.connect(**connection_params) as conn, open('tmp.csv', mode='rt') as f:
    cursor = conn.cursor()
    cursor.copy_from(f, 'employee', sep=',')
    conn.commit()

os.remove(temp_csv_name)
print('Processing took %s sec' % (time() - init_time))