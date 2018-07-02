from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, json, send_file
from flask_mail import Mail, Message
import os
from urllib.parse import urlparse
import psycopg2

# only for local image rendering
# from PIL import Image

import base64
from io import BytesIO

#file with helper functions
#import functions

import json

#for current date
import datetime

import ast

app = Flask(__name__)

#app.secret_key = os.environ['SECRET_KEY']
app.secret_key = '\x12\x9e8/\xfb\x86p\x91\xd9\xf2\xac\xf8U\xf1\xc87`\x87\x95\x18*)\xb2\xac'

#configuring upload_folder variable
app.config['UPLOAD_FOLDER'] = "/tmp/"

app.config.update(
    # DEBUG=True,
    #EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'crunch.thracker@gmail.com',
    #MAIL_PASSWORD = os.environ['epassword']
    MAIL_PASSWORD = 'crunchthracker'
    )
mail = Mail(app)

#configuring database url and path
#url = urlparse(os.environ['DATABASE_URL'])
url = urlparse('postgres://mbgugkwmyyrgpp:08f1f171ba8df81468de5e7d166069757cc545fb163d5cc820407068513b101d@ec2-54-163-237-249.compute-1.amazonaws.com:5432/da0io40vrbg6u0')


db = "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname)
schema = "schema.sql"
#connecting a cursor for the database
conn = psycopg2.connect(db)
cursor = conn.cursor()

#welcome page rendering
@app.route('/')
def welcome():
    error = request.args.get('error')
    return render_template('login.html', error=error)

#rendering registration page
@app.route('/register')
def newUser():
    error = request.args.get('error')
    return render_template('register.html', error=error)

#method after clicking on login button
@app.route('/postlogin', methods=['POST'])
#method for logging in, on home page.
def login():
    #verify the credentials

    # if login was successful, set this to the user's email
    # TODO
    session['user'] = 'howdy@gmail.com'
    # if user email exists in the admin table
    # if user email isCurator flag is marked
    # these yield different views
    return redirect(url_for('loggedin'))

#rendering home page after logging in
@app.route('/home')
def loggedin():
    error = request.args.get('error')
    museumname = request.form.get('museumname')
    return render_template('home.html', museum_name=museumname, error=error)

@app.route('/postregister', methods=['POST'])
def register():
    return redirect(url_for('loggedin'))

@app.route('/allMuseums', methods=['POST'])
def allMuseums():
    return render_template('allMuseums.html')

@app.route('/museum', methods=["POST"])
def getMuseumName():
    museum_name = request.form.get('museumname')
    museum_name_dropdown = request.form.get('museumnamedropdown')
    print("Museuem name: " + museum_name)
    #TODO: make a museum_name_dropdown
    # if museum_name is '' and museum_name_dropdown is '':
    if museum_name is '':
        error = "Must enter/select a museum name!"
        return redirect(url_for('loggedin', error=error))
    # elif museum_name is not '' and museum_name not in list of museums:
    #     error = "The museum you have entered does not exist!"
    #     return redirect(url_for('loggedin', error=error))
    else:
        return redirect(url_for('specificMuseum', museum_name=museum_name))

@app.route('/museum/<museum_name>', methods=['POST', "GET"])
def specificMuseum(museum_name):
    museumname = museum_name
    return render_template('specificMuseum.html', museum_name=museumname)

@app.route('/viewReviews/<museum_name>', methods=['POST'])
def viewReviews(museum_name):
    museum_name = museum_name
    return render_template('viewReviews.html', museum_name=museum_name)

@app.route('/back')
def back():
    return redirect(url_for('loggedin'))

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