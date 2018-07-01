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
    # print (repr(error))
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
    return redirect(url_for('loggedin'))

#rendering home page after logging in
@app.route('/home', methods=["GET"])
def loggedin():
    museumname = request.form.get('museumname')
    return render_template('home.html', museum_name=museumname)

@app.route('/postregister', methods=['POST'])
def register():
    return redirect(url_for('loggedin'))

@app.route('/postselectAllMuseums', methods=['POST'])
def allMuseums():
    return render_template('allMuseums.html')

@app.route('/museum', methods=["POST"])
def getMuseumName():
    museum_name = request.form.get('museumname')
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


if __name__ == "__main__":
    app.jinja_env.add_extension('jinja2.ext.do')
    app.debug = True
    app.run()

# 