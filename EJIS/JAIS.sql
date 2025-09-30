use journals;
create table JAIS(
	ID INT auto_increment primary key,
	Title varchar(255),
    Year varchar(255),
    ArticleURL varchar(255),
    Abstarct TEXT,
    Author_Name varchar(255),
    Author_University varchar(255));

alter table JAIS
add column Author_State varchar(255);

alter table JAIS
add column Author_Country varchar(255);

select count(distinct Author_University) from JAIS;

select distinct jas.Author_University,js.Author_State,js.Author_Country from JAIS jas join JSIS js join Journal_Articles ja on jas.Author_University=js.Author_University and jas.Author_University=ja.Author_University ORDER BY jas.Author_University;