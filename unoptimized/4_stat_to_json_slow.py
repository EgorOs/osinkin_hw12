#!/usr/bin/env python3

import psycopg2
import json
from time import time

def frq_fname_lname(connection_params: dict) -> str:
    with psycopg2.connect(**connection_params) as conn:
        cursor = conn.cursor()
        sql = """
        SELECT concat(first_name, ' ', last_name) AS paired_names
        FROM employee
        GROUP BY paired_names
        ORDER BY COUNT(*) DESC, paired_names
        LIMIT 1;
        """
        cursor.execute(sql)
        res = cursor.fetchall()

    return res[0][0]


def work_outside_dep_city(connection_params: dict) -> int:
    with psycopg2.connect(**connection_params) as conn:
        cursor = conn.cursor()
        sql = """
        SELECT COUNT(*) 
        FROM(        
            SELECT employee_city, employee_department, department_city 
            FROM employee JOIN department 
            ON employee_department = department_id
            WHERE employee_city <> department_city) as records
        """
        cursor.execute(sql)
        res = cursor.fetchall()

    return res[0][0]


def earns_more_than_boss(connection_params: dict) -> int:
    with psycopg2.connect(**connection_params) as conn:
        cursor = conn.cursor()
        sql = """
        SELECT count(employee_id)
        FROM(
            SELECT boss_emp.salary, boss_emp.employee_id, worker.boss, worker.salary
            FROM employee boss_emp
            JOIN employee worker
            ON boss_emp.employee_id = worker.boss
            WHERE boss_emp.salary < worker.salary) AS records
        """
        cursor.execute(sql)
        res = cursor.fetchall()

    return res[0][0]


def highest_salary_dep(connection_params: dict) -> str:
    with psycopg2.connect(**connection_params) as conn:
        cursor = conn.cursor()
        sql = """
        SELECT department_name
        FROM department
        WHERE department_id = (
            SELECT employee_department 
            FROM employee
            GROUP BY employee_id, employee_department
            ORDER BY AVG(salary) DESC
            LIMIT 1);
        """
        cursor.execute(sql)
        res = cursor.fetchall()

    return res[0][0]


def most_diff_salary_by_dep(connection_params: dict) -> list:
    """
    Percentage based selection found at
    https://stackoverflow.com/questions/24626036/postgresql-
    how-do-i-select-top-n-percent-entries-from-each-group-category
    """
    with psycopg2.connect(**connection_params) as conn:
        cursor = conn.cursor()
        sql = """
        WITH top_and_low AS (
        SELECT employee_department, salary,
        row_number() over (partition by employee_department ORDER BY salary DESC) AS rn,
        count(*) over (partition by employee_department) AS cnt
        FROM employee),
        top_sum AS (
        SELECT employee_department, sum(salary) FROM top_and_low
        WHERE (rn+0.0)/cnt <= 0.1
        GROUP BY employee_department),
        low_sum AS (
        SELECT employee_department, sum(salary) from top_and_low
        WHERE (rn+0.0)/cnt >= 0.9
        GROUP BY employee_department),
        diff_pair AS (SELECT N.employee_department, N.sum, M.sum FROM low_sum N
        JOIN top_sum M ON N.employee_department = M.employee_department
        ORDER BY (M.sum+0.0)/N.sum DESC
        LIMIT 2)
        SELECT department_name FROM department
        JOIN diff_pair ON department_id = employee_department
        """
        cursor.execute(sql)
        res = cursor.fetchall()
        res = [i[0] for i in res]
    return res


connection_params = {
    'host': 'localhost',
    'port': '5431',
    'user': 'root',
    'password': 'password',
    'dbname': 'homework'
}

init_time = time()
results = {
'hw1': frq_fname_lname(connection_params),
'hw2': work_outside_dep_city(connection_params),
'hw3': earns_more_than_boss(connection_params),
'hw4': highest_salary_dep(connection_params),
'hw5': most_diff_salary_by_dep(connection_params)
}

results_json = json.dumps(results, sort_keys=True, indent=4, separators=(',', ':'))
print(results_json)
print('Processing took %s sec' % (time() - init_time))

