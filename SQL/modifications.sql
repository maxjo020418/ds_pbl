-- primary key 추가
alter table library_data
    add column id int not null auto_increment primary key first;

-- Geodata point 추가 (위도, 경도)
alter table library_data
    add column geo_point point;

-- update library_data
--     set geo_point = point(위도, 경도);

create table library_reviews (
    id int primary key auto_increment,
    library_id int,
    url varchar(100),
    review text,
    foreign key (library_id) references library_data(id)
);

-- -------------

use datascience_pbl;

delete from library_reviews where true;

-- backup
CREATE TABLE library_reviews_backup LIKE library_reviews;
INSERT INTO library_reviews_backup SELECT * FROM library_reviews;

-- Drop the old id column
ALTER TABLE library_reviews
    DROP COLUMN id;

-- Add a new id column at the front, set as AUTO_INCREMENT PRIMARY KEY
ALTER TABLE library_reviews
    ADD COLUMN id INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;

-- ----------------------------------------------------------------------

ALTER TABLE library_reviews
    ADD INDEX idx_library_id (library_id);

ALTER TABLE library_reviews
    MODIFY COLUMN library_id INT NULL;

ALTER TABLE library_reviews
    ADD CONSTRAINT fk_library_reviews_library
        FOREIGN KEY (library_id)
            REFERENCES library_data(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE;
