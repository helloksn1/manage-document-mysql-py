# create database document;

create table user (
    id int primary key auto_increment,
    name varchar(255) unique,
    password varchar(255) not null
);

create table document (
    id int primary key auto_increment,
    name varchar(255) not null,
    time datetime default now(),
    type int not null,
    position varchar(255),
    content text
);

insert into user(name, password) values('admin', 'admin');
