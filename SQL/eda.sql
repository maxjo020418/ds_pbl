SELECT COUNT(`도서관명`) AS "위경도 있음"
FROM `library_data`
WHERE
	`위도` IS NOT NULL AND
    `경도` IS NOT NULL;


SELECT COUNT(`도서관명`) AS "필수자료 있음"
FROM `library_data`
WHERE
	`위도` IS NOT NULL AND
    `경도` IS NOT NULL AND
    `시도명` IS NOT NULL AND
    `시군구명` IS NOT NULL;

