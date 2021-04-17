#show databases;
create database IF NOT EXISTS kfk;
use kfk;

drop table if exists getDetail;
drop table if exists login;
drop table if exists buy;
drop table if exists cart;

create table  if not exists getDetail(
    id INT PRIMARY KEY  AUTO_INCREMENT,
    sessionId varchar(50),
    date DATETIME,
    userId LONG,
    itemId LONG,
    categoryId LONG

);

#drop table if exists login;
create table  if not exists buy(
    id INT PRIMARY KEY NOT NULL  AUTO_INCREMENT,
    sessionId varchar(50),
    date DATETIME,
    userId LONG,
    itemId LONG,
    categoryId LONG,
    isSecondKill int,
    success int
);

create table  if not exists login(
    id INT PRIMARY KEY NOT NULL  AUTO_INCREMENT,
    sessionId varchar(50),
    date DATETIME,
    userId LONG,
    success int,
    ipAddr varchar(20)
);

create table  if not exists cart(
    id INT PRIMARY KEY NOT NULL  AUTO_INCREMENT,
    sessionId varchar(50),
    date DATETIME,
    userId LONG,
    itemId LONG,
    categoryId LONG
);

create table  if not exists favor(
    id INT PRIMARY KEY NOT NULL  AUTO_INCREMENT,
    sessionId varchar(50),
    date DATETIME,
    userId LONG,
    itemId LONG,
    categoryId LONG
);