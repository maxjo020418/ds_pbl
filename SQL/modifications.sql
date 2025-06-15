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

