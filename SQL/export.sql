SHOW VARIABLES LIKE 'secure_file_priv';

SELECT *
INTO OUTFILE '/var/lib/mysql-files/reviews.csv'
    FIELDS TERMINATED BY ','
    ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
FROM library_reviews;