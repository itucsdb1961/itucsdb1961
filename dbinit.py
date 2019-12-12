import os
import sys

import psycopg2 as dbapi2

url = "postgres://vzvhmhqevlcedf:141b03607dee6c5c995d91b952b06e4fc122006f5cd2c1d789403aae34dc40a1@ec2-54-217-225-16.eu-west-1.compute.amazonaws.com:5432/dafo7esm4hjfc7"
secret_key = "hjkalsfdlamfrqwrxzc"

def init_book_table(url):
	statement = '''
		CREATE TABLE BOOKS(
			ID SERIAL,
			NAME VARCHAR(80) NOT NULL,
			PB_YR CHAR(4) NOT NULL,
			PB_LOC VARCHAR(80),
			PUBLISHER VARCHAR(80),
			GENRE VARCHAR(20),
			LANG VARCHAR(20),


			UNIQUE(NAME,PB_YR),
			PRIMARY KEY(ID)

		)'''
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute("DROP TABLE IF EXISTS BOOKS")
		connection.commit()

	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(statement)
		connection.commit()


def init_author_table(url):

	statement = '''
		CREATE TABLE AUTHORS(
			ID SERIAL,
			NAME VARCHAR(40) NOT NULL,
			LAST_NAME VARCHAR(40) NOT NULL,
			BIRTH_YR CHAR(4),
			BIRTH_PLACE VARCHAR(40),
			LAST_BOOK_DATE VARCHAR(40),
			LAST_BOOK_NAME VARCHAR(40),
	
			UNIQUE(NAME, LAST_NAME),
			PRIMARY KEY(ID)
		)'''

	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute("DROP TABLE IF EXISTS AUTHORS")
		connection.commit()
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(statement)
		connection.commit()


def init_student_table(url):

	statement = '''
		CREATE TABLE STUDENTS(
			ID SERIAL,
			NAME VARCHAR(40) NOT NULL,
			LAST_NAME VARCHAR(40) NOT NULL,
			FACULTY VARCHAR(40) NOT NULL,
			DEPART VARCHAR(40) NOT NULL,
			GRADE INTEGER NOT NULL,
			MEM_DATE VARCHAR(40),
			DEBT FLOAT,

			PRIMARY KEY(ID)
		)'''
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute("DROP TABLE IF EXISTS STUDENTS")
		connection.commit()
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(statement)
		connection.commit()
		
def init_relation_table_book_author(url):
	
	statement = '''
		CREATE TABLE BOOK_AUTHORS(
			BOOK_ID INT  REFERENCES BOOKS(ID),
			AUTHOR_ID INT REFERENCES AUTHORS(ID),
			
			UNIQUE (BOOK_ID,AUTHOR_ID),
			PRIMARY KEY(BOOK_ID,AUTHOR_ID)			
		)'''
	
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute("DROP TABLE IF EXISTS BOOK_AUTHORS")
		connection.commit()
		
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(statement)
		connection.commit()

def init_closets_table(url):

	statement = '''
		CREATE TABLE CLOSETS(
			ID SERIAL,
			CLOSET_FLOOR VARCHAR(40) NOT NULL,
			BLOCK VARCHAR(40) NOT NULL,
			CLOSET_NUMBER VARCHAR(40) NOT NULL,
			CLOSET_TYPE VARCHAR(40) NOT NULL,
			SIZE VARCHAR(40) NOT NULL,
			RETURN_HOUR CHAR(40) NOT NULL,

			UNIQUE(CLOSET_FLOOR,CLOSET_NUMBER),
			PRIMARY KEY(ID)
		)'''
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute("DROP TABLE IF EXISTS CLOSETS")
		connection.commit()
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(statement)
		connection.commit()

def init_db(url):
	init_book_table(url)
	init_author_table(url)
	init_student_table(url)
	init_closets_table(url)
	init_relation_table_book_author(url)

#init_db(url)
