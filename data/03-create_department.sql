CREATE TABLE IF NOT EXISTS department (
    department_id SERIAL NOT NULL PRIMARY KEY,
    department_name VARCHAR(255) NOT NULL,
    department_city INTEGER REFERENCES city(city_id)
);

-- INSERT INTO db_scheme_version(db_version, upgraded_on) VALUES ('1.2', now());

UPDATE db_scheme_version
SET db_version = '1.2', upgraded_on = NOW()