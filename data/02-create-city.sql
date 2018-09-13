CREATE TABLE IF NOT EXISTS city (
    city_id SERIAL NOT NULL PRIMARY KEY,
    city_name VARCHAR(255) NOT NULL UNIQUE
);


-- INSERT INTO db_scheme_version(db_version, upgraded_on) VALUES ('1.1', now());
-- Update instead of insert, to keep only one value

UPDATE db_scheme_version
SET db_version = '1.1', upgraded_on = NOW()
