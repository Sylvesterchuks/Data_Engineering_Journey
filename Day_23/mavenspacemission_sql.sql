CREATE DATABASE mavenspacemission;

USE mavenspacemission;

DROP TABLE allmissions;

-- Create all missions table
CREATE TABLE allmissions (
	Company VARCHAR(45),
    Location VARCHAR(255),
    Date DATE,
    Time TIME,
    Rocket VARCHAR(255),
    Mission VARCHAR(255),
    RocketStatus VARCHAR(45),
    Price VARCHAR(45),
    MissionStatus VARCHAR(25)
);

LOAD DATA LOCAL INFILE 'E:/cdrive/data_world/data_science/maven/space mission/Space+Missions/space_missions.csv'
INTO TABLE allmissions
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


-- Error Code: 3948. Loading local data is disabled; this must be enabled on both the client and server sides
-- Error Code: 2068. LOAD DATA LOCAL INFILE file request rejected due to restrictions on access.

SET GLOBAL local_infile=1;

SHOW GLOBAL VARIABLES LIKE 'local_infile';


/*



*/
-- display all records in the table
SELECT * FROM allmissions;

-- create a launchlocation table
CREATE TABLE launchlocations (
SELECT DISTINCT SUBSTR(TRIM(location), 1, LENGTH(location) - LENGTH(SUBSTRING_INDEX(location, ',', -1))-1) AS address,
		location,
        CASE 
			WHEN SUBSTRING_INDEX(SUBSTRING_INDEX(location, ',', -2), ',', 1) LIKE '%CENTER%' THEN SUBSTRING_INDEX(TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(location, ',', -2), ',', 1)), ' ', 1)
			ELSE SUBSTRING_INDEX(SUBSTRING_INDEX(location, ',', -2), ',', 1)
        END AS state,
        SUBSTRING_INDEX(location, ',', -1) AS country
        -- SUBSTRING_INDEX(SUBSTRING_INDEX(location, ',', -2), ',', 1)
FROM allmissions
ORDER BY 1
);

-- Alter the table, add a new column and make it a primary key
ALTER TABLE launchlocations 
ADD COLUMN launch_id INT auto_increment not null primary key first; 

-- display records in launchlocations
SELECT * FROM launchlocations;

-- create a rocketinfo table
CREATE TABLE rocketinfo (
SELECT DISTINCT rocket,
		rocketstatus
FROM allmissions
ORDER BY 1);

-- Alter the table, add a new column and make it a primary key
ALTER TABLE rocketinfo 
ADD COLUMN rocket_id INT auto_increment not null primary key first; 

-- display records in rocketinfo
SELECT * FROM rocketinfo;


-- create a missions table
CREATE TABLE missions (
SELECT DISTINCT mission,
        missionstatus
FROM allmissions
ORDER BY 1);

-- Alter the table missions, add a new column and make it a primary key
ALTER TABLE missions 
ADD COLUMN mission_id INT auto_increment not null primary key first; 

-- display records in missions
SELECT * FROM missions;


-- display records in companies
CREATE TABLE companies (
SELECT DISTINCT company
		-- TRIM(SUBSTRING_INDEX(location, ',', -1)) AS country
FROM allmissions
ORDER BY 1);

-- Alter the table companies, add a new column and make it a primary key
ALTER TABLE companies 
ADD COLUMN company_id INT auto_increment not null primary key first; 

-- display records in companies
SELECT * FROM companies;



-- create a allmissions_normalized table
CREATE TABLE space_missions (
SELECT c.company_id, 
		ll.launch_id, 
        am.date, 
        am.time, 
        ri.rocket_id, 
        m.mission_id, 
        COALESCE(REPLACE(am.price, ',', ''), NULL) AS price
FROM allmissions am
JOIN companies c 
	ON c.company = am.company
JOIN launchlocations ll
	ON am.location = ll.location
JOIN rocketinfo ri
	ON ri.rocket= am.rocket AND ri.rocketstatus = am.rocketstatus
JOIN missions m
	ON m.mission = am.mission AND m.missionstatus = am.missionstatus
);



-- Alter the table missions, add a new column and make it a primary key
ALTER TABLE space_missions 
ADD COLUMN space_mission_id INT auto_increment not null primary key first,
MODIFY price DECIMAL(10,2);

/* 
	If you encounter this Error Code: 1366. Incorrect DECIMAL value: '0' for column '' at row -1. 
    comment out and run the next statement, then rerun the Alter statement.
*/
-- SET SESSION sql_mode ='';
-- SET SESSION sql_mode = 'ONLY_FULL_GROUP_BY,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION'; 

 

-- display records in missions
SELECT * FROM space_missions;


-- Add foreign key to create relationship and reference other tables
ALTER TABLE space_missions
ADD CONSTRAINT `mission_details_fk`
    FOREIGN KEY (`mission_id`)
    REFERENCES `mavenspacemission`.`missions` (`mission_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
ADD CONSTRAINT `launchlocation_mission_fk`
    FOREIGN KEY (`launch_id`)
    REFERENCES `mavenspacemission`.`launchlocations` (`launch_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
ADD CONSTRAINT `companies_incharge_fk`
    FOREIGN KEY (`company_id`)
    REFERENCES `mavenspacemission`.`companies` (`company_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
ADD CONSTRAINT `rocket_used_in_mission_fk`
    FOREIGN KEY (`rocket_id`)
    REFERENCES `mavenspacemission`.`rocketinfo` (`rocket_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION;

-- DROP DATABASE mavenspacemission;