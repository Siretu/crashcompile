/* 
Initialize the database and its tables.
You may want to drop the database before running this script to start out fresh.

> drop database crashcompile;
*/

create database crashcompile;

use crashcompile;

create table party (
       id int unsigned primary key auto_increment,
       current_problem int
);

create table user (
       id int unsigned primary key auto_increment,
       session_id binary(16) not null unique,
       party_id int unsigned,
       name varchar(16)
);

create table problem (
       id int unsigned primary key auto_increment,
       nrTests int
);

insert into problem values (1, 5);
insert into party values (3, 1);

SET GLOBAL TRANSACTION ISOLATION LEVEL READ COMMITTED