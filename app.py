from __future__ import print_function
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, json, send_file
import os, mysql.connector
from mysql.connector import errorcode
from urllib.parse import urlparse

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
    print(e.msg)

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
    "   `isCurator` bit NOT NULL,"
    "   PRIMARY KEY (`email`),"
    "   CONSTRAINT CHK_CVV CHECK (CVV BETWEEN 100 AND 9999),"
    "   CONSTRAINT CHK_Month CHECK (Month BETWEEN 1 AND 12)"
    ")")

TABLES['museum'] = (
    "CREATE TABLE `museum` ("
    "   `museumName` varchar(255) NOT NULL,"
    "   `curatorEmail` varchar(255) NOT NULL,"
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
    isCurator = None
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
        print(e.msg)
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
    museumname = request.form.get('museumname')
    isCurator = request.args.get('isCurator')
    isAdmin = request.args.get('isAdmin')
    email = request.args.get('email')
    return render_template('home.html', museum_name=museumname, isCurator=isCurator, isAdmin=isAdmin, email=email, error=error)

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




    query = "INSERT into visitor values ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}');".format(email, password, cardNumber, month, year, cvv, isCurator)
    
    try:
        cursor.execute(query)
    except Exception as e:
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

@app.route('/museum/<museum_name>', methods=['POST', "GET"])
def specificMuseum(museum_name):
    museumname = museum_name
    isCurator = request.args.get('isCurator')
    museum_info = None

    query = "SELECT exhibitName, year, url FROM museumdb.exhibit WHERE museumName = '{0}';".format(museumname)

    try:
        cursor.execute(query)
        museum_info = cursor.fetchall()
        print(museum_info)
    except:
        print('error')

    return render_template('specificMuseum.html', museum_name=museumname, isCurator=isCurator, museum_info=museum_info)

@app.route('/viewReviews/<museum_name>', methods=['POST'])
def viewReviews(museum_name):
    museum_name = museum_name
    return render_template('viewReviews.html', museum_name=museum_name)

@app.route('/myAccount')
def manageAccount():
    return render_template('account.html')

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
    return render_template('myTickets.html')

@app.route('/myReviews')
def myReviews():
    return render_template('myReviews.html')

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

if __name__ == "__main__":
    app.jinja_env.add_extension('jinja2.ext.do')
    app.debug = True
    app.run()

# 
cursor.close()
# conn.commit()
conn.close()