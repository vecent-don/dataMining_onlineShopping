#show databases;
create database IF NOT EXISTS kfk;
use kfk;
create table  if not exists getDetail(
    id INT PRIMARY KEY NOT NULL  AUTO_INCREMENT,
    sessionId varchar(50),
    date DATETIME,
    userId LONG,
    itemId LONG,
    categoryId LONG

);

create table  if not exists buy(
    id INT PRIMARY KEY NOT NULL  AUTO_INCREMENT,
    sessionId varchar(50),
    date DATETIME,
    userId LONG,
    itemId LONG,
    categoryId LONG,
    isSecondKill int,
    succsess int
);

create table  if not exists login(
    id INT PRIMARY KEY NOT NULL  AUTO_INCREMENT,
    sessionId varchar(50),
    date DATETIME,
    userId LONG,
    succsess int
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