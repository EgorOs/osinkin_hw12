ALTER TABLE employee
    DROP COLUMN employee_city;

ALTER TABLE employee
    ADD employee_city VARCHAR(255) NOT NULL;

ALTER TABLE department
    DROP COLUMN department_city;

ALTER TABLE department
    ADD department_city VARCHAR(255) NOT NULL;

-- DROP TABLE city;
-- Drop cascade to drop linked objects
-- DROP TABLE city CASCADE;
DROP TABLE city CASCADE;

UPDATE db_scheme_version
SET db_version = '1.4', upgraded_on = NOW()


