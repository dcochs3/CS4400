from __future__ import print_function
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, json, send_file
import os, mysql.connector
from mysql.connector import errorcode
import datetime
from random import randint
import jackfunc as jf
#from urllib.parse import urlparse

#for current date
import datetime

app = Flask(__name__)
app.secret_key = '\x12\x9e8/\xfb\x86p\x91\xd9\xf2\xac\xf8U\xf1\xc87`\x87\x95\x18*)\xb2\xac'

#team password: jdrn4533
databaseName = 'museumDB'

config = {
	'user': 'root',
	'password': 'jdrn4533',
	'host': 'localhost',
	'raise_on_warnings': True,
	'use_pure': False
}

#connecting a cursor for the database
try:
	conn = mysql.connector.connect(**config)
	cursor = conn.cursor()
except Exception as e:
	print(e.msg)

initDB = "CREATE DATABASE IF NOT EXISTS {}".format(databaseName)
try:
	cursor.execute(initDB)
except Exception as e:
	print(str(e))

conn.database = databaseName

TABLES = {}
TABLES['admin'] = (
	"CREATE TABLE `admin` ("
	"   `email` varchar(255) NOT NULL,"
	"   `password` varchar(255) NOT NULL,"
	"   PRIMARY KEY (`email`)"
	")")

TABLES['visitor'] = (
	"CREATE TABLE `visitor` ("
	"   `email` varchar(255) NOT NULL,"
	"   `password` varchar(255) NOT NULL,"
	"   `cardNumber` char(16) NOT NULL UNIQUE,"
	"   `month` tinyint NOT NULL,"
	"   `year` char(4) NOT NULL,"
	"   `cvv` smallint NOT NULL,"
	"   `isCurator` boolean NOT NULL,"
	"   PRIMARY KEY (`email`),"
	"   CONSTRAINT CHK_CVV CHECK (CVV BETWEEN 100 AND 9999),"
	"   CONSTRAINT CHK_Month CHECK (Month BETWEEN 1 AND 12)"
	")")

TABLES['museum'] = (
	"CREATE TABLE `museum` ("
	"   `museumName` varchar(255) NOT NULL,"
	"   `curatorEmail` varchar(255),"
	"   PRIMARY KEY (`museumName`),"
	"   FOREIGN KEY (`curatorEmail`) REFERENCES `visitor` (`email`)"
	")")

TABLES['curator_request'] = (
	"CREATE TABLE `curator_request` ("
	"   `museumName` varchar(255) NOT NULL,"
	"   `visitorEmail` varchar(255) NOT NULL,"
	"   PRIMARY KEY (`museumName`, `visitorEmail`),"
	"   FOREIGN KEY (`museumName`) REFERENCES `museum` (`museumName`),"
	"   FOREIGN KEY (`visitorEmail`) REFERENCES `visitor` (`email`)"
	")")

TABLES['review'] = (
	"CREATE TABLE `review` ("
	"   `museumName` varchar(255) NOT NULL,"
	"   `visitorEmail` varchar(255) NOT NULL,"
	"   `comment` varchar(4096),"
	"   `rating` tinyint NOT NULL,"
	"   PRIMARY KEY (`museumName`, `visitorEmail`),"
	"   FOREIGN KEY (`museumName`) REFERENCES `museum` (`museumName`),"
	"   FOREIGN KEY (`visitorEmail`) REFERENCES `visitor` (`email`),"
	"   CONSTRAINT CHK_Rating CHECK (Rating BETWEEN 1 AND 5)"
	")")

TABLES['ticket'] = (
	"CREATE TABLE `ticket` ("
	"   `museumName` varchar(255) NOT NULL,"
	"   `visitorEmail` varchar(255) NOT NULL,"
	"   `price` decimal(7,2) NOT NULL,"
	"   `purchaseTimeStamp` datetime NOT NULL,"
	"   PRIMARY KEY (`museumName`, `visitorEmail`),"
	"   FOREIGN KEY (`museumName`) REFERENCES `museum` (`museumName`),"
	"   FOREIGN KEY (`visitorEmail`) REFERENCES `visitor` (`email`)"
	")")

TABLES['exhibit'] = (
	"CREATE TABLE `exhibit` ("
	"   `museumName` varchar(255) NOT NULL,"
	"   `exhibitName` varchar(255) NOT NULL,"
	"   `year` char(4) NOT NULL,"
	"   `url` varchar(2083),"
	"   `curatorEmail` varchar(255) NOT NULL,"
	"   PRIMARY KEY (`museumName`, `exhibitName`),"
	"   FOREIGN KEY (`museumName`) REFERENCES `museum` (`museumName`),"
	"   FOREIGN KEY (`curatorEmail`) REFERENCES `visitor` (`email`)"
	")")

# creating tables
for name, ddl in TABLES.items():
	try:
		print("Creating table {}: ".format(name), end='')
		cursor.execute(ddl)
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
			print("already exists.")
		else:
			print(err.msg)
	else:
		print("OK")




# TODO: cascading deletes??? These should go in the create table statements
# ASSERT (aka an email should not exist in both the admin and visitor table)
# I'm able to create a museum with an admin email that does not exist -- foreign key mapping isn't working?
# Make default table population so if we need to delete and remake a table (like in order to add cascading deletes, etc), we can easily add back the data
# Be aware of the "back" button (especially for different views -- if you're a curator and you go back and you can't see certain curator only buttons, thats a problem)










#welcome page rendering
@app.route('/')
def welcome():
	error = request.args.get('error')
	return render_template('login.html', error=error)
#method after clicking on login button
@app.route('/postlogin', methods=['POST'])
#method for logging in, on home page.
def login():
	#verify the credentials
	email = request.form['email']
	password = request.form['password']
	error = None
	visitor_list = None
	admin_list = None
	isAdmin = None

	query = "SELECT email FROM visitor WHERE email = '{0}' AND password = '{1}';".format(email, password)
	query1 = "SELECT isCurator FROM museumdb.visitor WHERE email = '{0}';".format(email);
	adminquery = "SELECT email FROM museumdb.admin WHERE email = '{0}' AND password = '{1}';".format(email, password)

	try:
		# from visitor table
		cursor.execute(query)
		visitor_list = cursor.fetchone()
		cursor.execute(query1)
		isCurator = cursor.fetchone()
		isCurator = isCurator[0]
		# from admin table
		cursor.execute(adminquery)
		admin_list = cursor.fetchone()


		if visitor_list is None and admin_list is None:
			# no email/pass combo exists in the database
			error = 'The email or password you have entered is incorrect.'
			return redirect(url_for('welcome', error=error))
		elif visitor_list is not None:
			# login was successful
			# the user is a normal user
			# set session value to the user email
			session['user'] = visitor_list[0]

			# this makes the session expire when the BROWSER is closed, not the tab/window
			session.SESSION_EXPIRE_AT_BROWSER_CLOSE = True
		else:
			# login was successful
			# the user is admin
			# set session value to the user email
			session['user'] = admin_list[0]

			# this makes the session expire when the BROWSER is closed, not the tab/window
			session.SESSION_EXPIRE_AT_BROWSER_CLOSE = True
			isAdmin = 1
	except Exception as e:
		print(str(e))
		query = "rollback;"
		cursor.execute(query)
		error = 'The email or password you have entered is incorrect.'
		return redirect(url_for('welcome', error=error))


	# TODO
	# if user email exists in the admin table
	# if user email isCurator flag is marked
	# these yield different views
	return redirect(url_for('loggedin', isCurator=isCurator, isAdmin=isAdmin, email=email))

#rendering home page after logging in
@app.route('/home')
def loggedin():
	error = request.args.get('error')
	isCurator = request.args.get('isCurator')
	museumname = request.form.get('museumname')
	isAdmin = request.args.get('isAdmin')
	email = session.get('user')
	museum_list = None
	no_museums = None

	query = "SELECT museumName FROM museum;"
	try:
		cursor.execute(query)
		museum_list = cursor.fetchall()

		if len(museum_list) == 0:
			no_museums = True

	except Exception as e:
		query = "rollback;"
		cursor.execute(query)
		print('error')

	return render_template('home.html', museum_list=museum_list, no_museums=no_museums, museum_name=museumname, isCurator=isCurator, isAdmin=isAdmin, email=email, error=error)

#rendering registration page
@app.route('/register')
def newUser():
	error = request.args.get('error')
	return render_template('register.html', error=error)

@app.route('/postregister', methods=['POST'])
def register():
	email = request.form['email']
	password = request.form['password']
	passwordcheck = request.form['password2']
	error = None
	isCurator = False

	cardNumber = request.form['cardnumber']
	month = request.form['exprmonth']
	year = request.form['expryear']
	cvv = request.form['seccode']

	if email == '' or password == '' or passwordcheck == '' or cardNumber == '' or month == '' or year == '' or cvv == '':
		error = 'Please fill in all fields.'
		return redirect(url_for('newUser', error=error))

	# do some email format checking
	# TODO

	# check passwords match
	if password != passwordcheck:
		error = 'Passwords do not match.'
		return redirect(url_for('newUser', error=error))

	# check valid cardNumber
	if cardNumber.isdigit() is False:
		# the card number entered contains non-numbers
		error = 'Please enter a valid credit card number.'
		return redirect(url_for('newUser', error=error))
	elif len(cardNumber) != 16:
		error = 'Please enter a valid credit card number.'
		return redirect(url_for('newUser', error=error))

	# check valid month
	if month.isdigit() is False:
		# the month entered contains non-numbers
		error = 'Please enter a valid credit card expiration month.'
		return redirect(url_for('newUser', error=error))
	elif len(month) != 2:
		error = 'Please enter the month as a two digit number.'
		return redirect(url_for('newUser', error=error))
	elif int(month) < 1 or int(month) > 12:
		error = 'Month must be between 1 and 12.'
		return redirect(url_for('newUser', error=error))

	# check valid year
	if year.isdigit() is False:
		# the year entered contains non-numbers
		error = 'Please enter a valid credit card expiration year.'
		return redirect(url_for('newUser', error=error))
	elif len(year) != 4:
		error = 'Please enter a valid credit card expiration year.'
		return redirect(url_for('newUser', error=error))
	elif int(year) < 2017 or int(year) > 9999:
		error = 'Please enter a valid credit card expiration year.'
		return redirect(url_for('newUser', error=error))

	# check valid cvv
	if cvv.isdigit() is False:
		error = 'Please enter a valid credit card security code.'
		return redirect(url_for('newUser', error=error))
	elif len(cvv) < 3 or len(cvv) > 4:
		error = 'Please enter a valid credit card security code.'
		return redirect(url_for('newUser', error=error))



	query = "INSERT into visitor values ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}');".format(email, password, cardNumber, month, year, cvv, int(isCurator))
	
	try:
		cursor.execute(query)
	except Exception as e:
		print(e.msg)
		query = "rollback;"
		cursor.execute(query)

		error = 'Account creation has failed.'
		return redirect(url_for('newUser', error=error))

	conn.commit() 
	return redirect(url_for('loggedin', isCurator=isCurator))

@app.route('/allMuseums', methods=['POST'])
def allMuseums():
	museum_list = None
	rating_list = None
	error = None
	isCurator = request.args.get('isCurator')

	query = "SELECT museumName FROM museum;"
	query1 = "SELECT museumName, AVG(rating) FROM review GROUP BY museumName;"

	try:
		cursor.execute(query)
		museum_list = cursor.fetchall()
		cursor.execute(query1)
		rating_list = cursor.fetchall()

		if museum_list is None:
			error = 'No museums currently exist.'
			return redirect(url_for('loggedin', error=error, isCurator=isCurator))

	except:
		query = "rollback;"
		cursor.execute(query)
		print('error')

	return render_template('allMuseums.html', museum_list=museum_list, isCurator=isCurator, rating_list=rating_list)

@app.route('/museum', methods=["POST"])
def getMuseumName():
	museum_name = request.form.get('museumname')
	museum_name_dropdown = request.form.get('museumnamedropdown')
	isCurator = request.args.get('isCurator')
	#TODO: make a museum_name_dropdown
	# if museum_name is '' and museum_name_dropdown is '':
	if museum_name is '':
		error = "Must enter/select a museum name!"
		return redirect(url_for('loggedin', error=error, isCurator=isCurator))
	# elif museum_name is not '' and museum_name not in list of museums:
	#     error = "The museum you have entered does not exist!"
	#     return redirect(url_for('loggedin', error=error))
	else:
		return redirect(url_for('specificMuseum', museum_name=museum_name, isCurator=isCurator))

@app.route('/museum/<museum_name>/<isCurator>', methods=['POST', "GET"])
def specificMuseum(museum_name, isCurator):
	museumname = museum_name
	museum_info = None
	museum_exists = None
	visitor_email = session.get('user')
	purchasedTicket = None
    query1 = "SELECT * FROM museumdb.museum WHERE museumName = '{0}';".format(museumname)
    query = "SELECT exhibitName, year, url FROM museumdb.exhibit WHERE museumName = '{0}';".format(museumname)
    purchasedTicketQuery = "SELECT * FROM ticket WHERE visitorEmail = '{0}' AND museumName = '{1}';".format(visitor_email, museumname)


	try:
		cursor.execute(query1)
		museum_exists = cursor.fetchone()
		cursor.execute(query)
		museum_info = cursor.fetchall()

		cursor.execute(purchasedTicketQuery)
		tickets = cursor.fetchall()

		if len(tickets) == 0:
			purchasedTicket = 0
		else:
			purchasedTicket = 1

	except:
		print('Error')

	if museum_exists is None:
		# that museum entered does not exist in the database
		error = "There is no museum with that name."
		return redirect(url_for('loggedin', error=error))
	print(type(isCurator))
	return render_template('specificMuseum.html', museum_name=museumname, isCurator=isCurator, museum_info=museum_info, purchasedTicket=purchasedTicket)

@app.route('/addExhibit/<museum_name>', methods=['POST'])       
def addExhibit(museum_name):
	museumname = museum_name
	exhibitname = request.form['exhibitname']
	year = request.form['year']
	link = request.form['link']
	isCurator = None
	museum_info = None
	curator_email = session.get('user')

	query =  "INSERT INTO exhibit VALUES ('{0}', '{1}', {2}, '{3}', '{4}');".format(museumname, exhibitname, year, link, curator_email)
	try:
		cursor.execute(query)
		conn.commit()
	except AttributeError as e:
		print(str(e))
	return redirect(url_for('specificMuseum', museum_name=museumname, isCurator=isCurator))

@app.route('/checkReviews/<museum_name>', methods=['GET'])
def checkReviews(museum_name):
	print("Got to Check Reviews")
	redirect(url_for("addReview", museum_name=museum_name, old_comment="", old_rating=-1))

@app.route('/addReview/<museum_name>/<comment>/<rating>', methods=['POST'])
def addReview(museum_name, old_comment, old_rating):

	comment = request.form['description']
	rating = request.form['rating']
	visitor_email = session.get('user')
	isCurator = None
	bought_ticket_query = "SELECT * FROM ticket WHERE museumName = '{0}' AND visitorEmail = '{1}'".format(museum_name, visitor_email)
	cursor.execute(bought_ticket_query)
	ticket = cursor.fetchall()
	bought_ticket = len(ticket) > 0
	if bought_ticket:
		select_review_query = "SELECT * FROM review WHERE museumName = '{0}' AND visitorEmail = '{1}';".format(museum_name, visitor_email)
		cursor.execute(select_query)
		review = cursor.fetchall()
		if len(review) > 0:
			print("already a review")
			#redirect(url_for())
		else:
			query = "INSERT INTO museumDB.review VALUES ('{0}', '{1}', '{2}', {3});".format(museum_name, visitor_email, comment, rating)
			cursor.execute(query)
			conn.commit()

	else:
		print("buy a ticket pls")
		#Tell the user they have to buy a ticket

	return redirect(url_for('specificMuseum', museum_name=museum_name, isCurator=isCurator)) 

@app.route('/viewReviews/<museum_name>', methods=['POST'])
def viewReviews(museum_name):
	museum_name = museum_name
	query = "SELECT * FROM museumdb.review WHERE museumName = '{0}';".format(museum_name)

	try:
		cursor.execute(query)
		reviews = cursor.fetchall()
	except:
		print('Error')    
	return render_template('viewReviews.html', reviews=reviews, museum_name=museum_name)

@app.route('/removeExhibit/<museum_name>/<exhibit_name>', methods=['POST'])
def removeExhibit(museum_name, exhibit_name):
	delete_query = "DELETE FROM exhibit WHERE exhibitName = '{0}' AND museumName = '{1}';".format(exhibit_name, museum_name)
	cursor.execute(delete_query)
	conn.commit()
	isCurator = True
	return redirect(url_for('specificMuseum', museum_name=museum_name, isCurator=isCurator))

@app.route('/purchasedTicket/<museum_name>', methods=['POST'])
def purchaseTicket(museum_name):
	museum_name = museum_name
	visitor_email = session.get('user')
	isCurator = request.args.get('isCurator')
	price = randint(0, 25)
	timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	query = "INSERT INTO museumdb.ticket (museumName, visitorEmail, price, purchaseTimeStamp) VALUES "
	query += "('{0}', '{1}', {2}, '{3}');".format(museum_name, visitor_email, price, timestamp)
	error = request.args.get('error')

	try:
		cursor.execute(query)
		conn.commit()
		error="Purchase successful."
	except Exception as e:
		print(e)

	return redirect(url_for('specificMuseum', museum_name=museum_name, isCurator=isCurator, error=error))

@app.route('/myAccount')
def manageAccount():
    email = session.get('user')
    isCurator = None

    query1 = "SELECT isCurator FROM museumdb.visitor WHERE email = '{0}';".format(email);

    try:
        cursor.execute(query1)
        isCurator = cursor.fetchone()
        isCurator = isCurator[0]

    except Exception as e:
        print(e.msg)
        query = "rollback;"
        cursor.execute(query)
        error = 'Error.'
        return redirect(url_for('welcome', error=error))

    return render_template('account.html', email=email, isCurator=isCurator)


@app.route('/back')
def back():
	isCurator = request.args.get('isCurator')
	return redirect(url_for('loggedin', isCurator=isCurator))

@app.route('/logout')
def logout():
	session.pop('user', None)
	return redirect(url_for('welcome'))

@app.route('/myTickets')
def myTickets():
	visitor_email = session.get('user')
	query = "SELECT * FROM ticket WHERE visitorEmail = '{0}';".format(visitor_email)
	cursor.execute(query)
	tickets = cursor.fetchall()
	conn.commit()
	return render_template('myTickets.html', tickets=tickets)

@app.route('/myReviews')
def myReviews():
	visitor_email = session.get('user')
	query = "SELECT * FROM review WHERE visitorEmail = '{0}';".format(visitor_email)
	cursor.execute(query)
	reviews = cursor.fetchall()
	conn.commit()
	return render_template('myReviews.html', reviews=reviews)

@app.route('/curatorRequest')
def curatorRequest():
	error = request.args.get('error')
	return render_template('curatorRequest.html', error=error)

@app.route('/postcuratorRequest', methods=["POST"])
def curatorRequested():
	# if TODO:
	# error = "You are already a curator for that museum!"

	error = "Request successfully submitted!"
	return redirect(url_for('curatorRequest', error=error))






# ADMIN FUNCTIONS (DANA)
# review curator requests
@app.route('/reviewCuratorRequests')
def reviewCuratorRequests():
	error = request.args.get('error')

	query = "SELECT * FROM museumdb.curator_request;"

	try:
		cursor.execute(query)
		curator_requests = cursor.fetchall()
	except Exception as e:
		print(e.msg)
		query = "rollback;"
		cursor.execute(query)
		error = 'There was an error retrieving curator requests.'
		return redirect(url_for('loggedin', isAdmin=1, email=session.get('user'), error=error))

	return render_template('reviewRequests.html', curator_requests=curator_requests, error=error)

@app.route('/adminHome')
def adminHome():
	error = request.args.get('error')
	return redirect(url_for('loggedin', isAdmin=1, email=session.get('user'), error=error))

@app.route('/approveRequest/<email>', methods=['POST'])
def approveRequest(email):
	email = email

	# update the visitor table
	updateQuery = "UPDATE museumdb.visitors SET isCurator=1 WHERE email='{0}';".format(email)
	# remove the request from the curator request table
	deleteQuery = "DELETE FROM museumdb.curator_request WHERE visitorEmail='{0}';".format(email)

	query = "SELECT * FROM museumdb.curator_request;"

	try:
		cursor.execute(updateQuery)
		error = "Request successfully approved."
		conn.commit()
		cursor.execute(deleteQuery)
		conn.commit()

		cursor.execute(query)
		curator_requests = cursor.fetchall()

	except Exception as e:
		print(e.msg)
		query = "rollback;"
		cursor.execute(query)
		query2 = "SELECT * FROM museumdb.curator_request;"
		cursor.execute(query2)
		curator_requests = cursor.fetchall()
		error = 'There was an approving the curator requests.'

	return redirect(url_for('reviewCuratorRequests', curator_requests=curator_requests, error=error))

@app.route('/denyRequest/<email>', methods=['POST'])
def denyRequest(email):
	email=email

	# there is no update to be done
	# remove the request from the curator request table
	deleteQuery = "DELETE FROM museumdb.curator_request WHERE visitorEmail='{0}';".format(email)

	query = "SELECT * FROM museumdb.curator_request;"

	try:
		cursor.execute(deleteQuery)
		conn.commit()
		error = "Request successfully denied."

		cursor.execute(query)
		curator_requests = cursor.fetchall()

	except Exception as e:
		print(e.msg)
		query = "rollback;"
		cursor.execute(query)
		query2 = "SELECT * FROM museumdb.curator_request;"
		cursor.execute(query2)
		curator_requests = cursor.fetchall()
		error = 'There was an approving the curator requests.'

	return redirect(url_for('reviewCuratorRequests', curator_requests=curator_requests, error=error))

# add museum
@app.route('/addMuseum', methods=['POST'])
def addMuseum():
	museum_name = request.form['input-museumname']
	error = request.args.get('error')

	# if already exists, error
	selectQuery = "SELECT * FROM museumdb.museum WHERE museumName='{0}';".format(museum_name)

	# add to the database
	# museumName // curatorEmail
	insertQuery = "INSERT into museumdb.museum values ('{0}', NULL);".format(museum_name)

	try:
		cursor.execute(insertQuery)
		conn.commit()

		error = "Museum successfully added."
	except Exception as e:
		print(e.msg)
		query = "rollback;"
		cursor.execute(query)

		cursor.execute(selectQuery)
		museum = cursor.fetchone()
		if museum is not '':
			error = 'The museum already exists!'
		else:
			# if other error
			error = 'There was an error adding the museum.'

	return redirect(url_for('loggedin', error=error, isAdmin=1))

# delete museum
@app.route('/deleteMuseum')
def deleteMuseum():
	error = request.args.get('error')
	museum_list = None
	no_museums = None

	query = "SELECT museumName FROM museum;"
	try:
		cursor.execute(query)
		museum_list = cursor.fetchall()

		if len(museum_list) == 0:
			no_museums = True

	except Exception as e:
		query = "rollback;"
		cursor.execute(query)

	return render_template('deleteMuseum.html', error=error, museum_list=museum_list, no_museums=no_museums)

@app.route('/typeDeleteMuseum', methods=["POST"])
def typeDeleteMuseum():
	museum_name = request.form.get('museumname')
	print(museum_name)
	error = request.args.get('error')

	# check the museum they typed exists
	selectQuery = "SELECT * FROM museumdb.museum WHERE museumName='{0}';".format(museum_name)

	query = "DELETE FROM museumdb.museum WHERE museumName='{0}';".format(museum_name)
	try:
		cursor.execute(selectQuery)
		museum = cursor.fetchone()
		if museum_name == '':
			error = "Please enter/select a museum name."
			return redirect(url_for('deleteMuseum', error=error))
		if museum is None:
			error = "No museum exists with that name."
			return redirect(url_for('deleteMuseum', error=error))
		else:
			cursor.execute(query)
			conn.commit()
			error = "Museum successfully deleted!"
	except Exception as e:
		query = "rollback;"
		cursor.execute(query)
		error = "There was an error deleting the museum."

	return redirect(url_for('loggedin', error=error, isAdmin=1))


@app.route('/actionDeleteMuseum/<museum_name>')
def actionDeleteMuseum(museum_name):
	museum_name=museum_name
	error = request.args.get('error')

	query = "DELETE FROM museumdb.museum WHERE museumName='{0}';".format(museum_name)
	try:
		cursor.execute(query)
		conn.commit()
		error = "Museum successfully deleted!"
	except Exception as e:
		query = "rollback;"
		cursor.execute(query)
		error = "There was an error deleting the museum."

	return redirect(url_for('loggedin', error=error, isAdmin=1))

@app.route('/myMuseums')
def myMuseums():
	visitorEmail = session.get('user')
	query = "SELECT museumName FROM museum WHERE curatorEmail='{0}';".format(visitorEmail)
	query1 = "SELECT museumName, AVG(rating) FROM review GROUP BY museumName;"
	query2 = "SELECT museumName, COUNT(exhibitName) FROM exhibit GROUP BY museumName;"

	try:
		cursor.execute(query)
		museum_list = cursor.fetchall()
		cursor.execute(query1)
		averageRatings = cursor.fetchall()
		cursor.execute(query2)
		exhibitCounts = cursor.fetchall()
	except Exception as e:
		query = "rollback;"
		cursor.execute(query)

	return render_template('myMuseums.html', museum_list=museum_list, averageRatings=averageRatings, exhibitCounts=exhibitCounts)

if __name__ == "__main__":
	app.jinja_env.add_extension('jinja2.ext.do')
	app.debug = True
	app.run()

# 
cursor.close()
# conn.commit()
conn.close()
