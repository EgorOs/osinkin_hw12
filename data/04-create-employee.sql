CREATE TABLE IF NOT EXISTS employee (
    employee_id SERIAL NOT NULL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    employee_department INTEGER REFERENCES department(department_id) NOT NULL,
    employee_city INTEGER REFERENCES city(city_id) NOT NULL,
    boss INTEGER REFERENCES employee(employee_id) NULL,
    salary DECIMAL(10, 2)
);

-- INSERT INTO db_scheme_version(db_version, upgraded_on) VALUES ('1.3', now());

UPDATE db_scheme_version
SET db_version = '1.3', upgraded_on = NOW()


