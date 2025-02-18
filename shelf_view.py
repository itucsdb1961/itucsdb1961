url = "postgres://mrzogiikkbrxmf:b6042668a00f9ea7e4d353f06e02e8c5ffab90a6a2a76191de8597340a254d68@ec2-54-228-243-29.eu-west-1.compute.amazonaws.com:5432/dsbe8b5jahoaq"
secret_key = "hjkalsfdlamfrqwrxzc"

import psycopg2 as dbapi2
from flask import Flask, request, redirect, url_for,render_template ,session, abort
from random import randint

class mshelf:
	def __init__(self,
				name,
				num,
				block,
				flr,
				capacity = 0,
				book_genre = ""):
		self.name = name
		self.num = num
		self.block = block
		self.flr = flr
		self.capacity = capacity
		self.book_genre = book_genre

	def add_to_db(self,db_url):
		STATEMENT ='''
					INSERT INTO
					SHELVES	(NAME, NUM, BLOCK, FLR, BOOK_GENRE, CAPACITY)
					VALUES 	('%s',%d, %d, %d, '%s', %d)
					ON CONFLICT DO NOTHING
					''' % (self.name, self.num, self.block, self.flr, self.book_genre, self.capacity)

		with dbapi2.connect(db_url) as connection:
			cursor = connection.cursor()
			cursor.execute(STATEMENT)
			connection.commit()


def admin_shelves_page():

	if not "access_level" in session or session["access_level"] > 2: # non-admin-user trying url manually / abort
		abort(451)

	shelves = []
	book_counts = []

	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute("select * from shelves")
		shelves = cursor.fetchall()

	if request.method == "POST":
		if "form_name" in request.form:
			if request.form["form_name"] == "shelf_create": 

				if request.form["capacity"]:
					tmp_shelf = mshelf(str(request.form["shelf_name"]),int(request.form["num"]),int(request.form["block"]),int(request.form["floor"]),int(request.form["capacity"]),str(request.form["book_genre"]))
					tmp_shelf.add_to_db(url)
				else:
					tmp_shelf = mshelf(str(request.form["shelf_name"]),int(request.form["num"]),int(request.form["block"]),int(request.form["floor"]),0,str(request.form["book_genre"]))
					tmp_shelf.add_to_db(url)

				with dbapi2.connect(url) as connection:
					cursor = connection.cursor()
					cursor.execute("select * from shelves")
					shelves = cursor.fetchall()

			elif request.form["form_name"] == "filter": # add shelve FORM SUBMITTED

				statement = '''
					SELECT * FROM SHELVES
				'''

				cond = []
	
				if request.form["genre"]:
					cond.append("(BOOK_GENRE ~* '.*" + str(request.form["genre"]) + ".*')")

				if request.form["shelf_floor"]:
					cond.append('''
						(FLR = '%s')
						''' % (str(request.form["shelf_floor"]))
					)
				if request.form["capacity"]:
					val = int(request.form["capacity"])
					cnd = '''
						(CAPACITY >= %d)
					''' % (int(val))
					cond.append(cnd)

				if len(cond):

					statement += " WHERE "

					first = True
					for cnd in cond:
						if not first:
							statement += " AND "
						first = False
						statement += cnd

				cursor.execute(statement)
				shelves = cursor.fetchall()

			elif request.form["form_name"] == "checkbox_filter":

				checkbox_cond = request.form.getlist("shelf_key")

				statement = "DELETE FROM SHELVES WHERE "
				update_statement = ""
				first = True
				for update in checkbox_cond:
					if not first:
						update_statement += " OR "
					update_statement += "ID = " + str(update)
					first = False

				statement += update_statement
				with dbapi2.connect(url) as connection:
					cursor = connection.cursor()
					cursor.execute(statement)

	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		if not (request.method == "POST" and request.form["form_name"] == "filter"):
			cursor.execute("select * from shelves")
			shelves = cursor.fetchall()

		idx = 0
		for shelf in shelves:
			book_counts.append([])
			cursor.execute('''
				SELECT * FROM SHELF_BOOKS
				WHERE SHELF_ID = %d
			''' % (int(shelf[0])))

			book_counts[idx].append(len(cursor.fetchall()))
			idx+=1

		for idx in range(0,len(shelves)):
			shelves[idx] = shelves[idx] + tuple(book_counts[idx])

	return render_template("admin_shelves.html", shelves = shelves, shelf_count = len(shelves), book_count = book_counts)

def shelf_page(shelf_id):
	shelf = []

	if request.method == "POST":
		if "form_name" in request.form:
			if request.form["form_name"] == "shelf_update":

				updates = []

				if request.form["num"]:
					updates.append("NUM = " + str(int(request.form["num"])))

				if request.form["block"]:
					updates.append("BLOCK = " + str(int(request.form["block"])))

				if request.form["floor"]:
					updates.append("FLR = " + str(int(request.form["floor"])))

				if request.form["genre"]:
					updates.append("BOOK_GENRE = " + "'" + str(request.form["genre"]) + "'")

				if request.form["capacity"]:
					updates.append("CAPACITY = " + str(int(request.form["capacity"])))

				if len(updates):

					statement = "UPDATE SHELVES SET "

					update_statement = ""
					first = True
					for update in updates:
						if not first:
							update_statement += " , "
						update_statement += update
						first = False

					statement += update_statement

					where_statement = ''' WHERE ID = %d
								''' % (int(shelf_id))

					statement += where_statement

					print(statement)

					with dbapi2.connect(url) as connection:
					 	cursor = connection.cursor()
					 	cursor.execute(statement)


	books = []

	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute('''
				select * from shelves
				where ID = %d
				''' % (int(shelf_id)))
		shelf = cursor.fetchall()[0]

		cursor.execute('''
			SELECT * FROM SHELF_BOOKS
			WHERE SHELF_ID = %d
		'''% (int(shelf_id))
		)		
		book_ids = cursor.fetchall()

		for book_id in book_ids:
			cursor.execute('''
				SELECT * FROM BOOKS
				WHERE ID = %d
			'''% (int(book_id[0]))
			)
			tmp_book = cursor.fetchall()[0]
			books.append(tmp_book)


	return render_template("shelf.html", shelf = shelf , books = books)
