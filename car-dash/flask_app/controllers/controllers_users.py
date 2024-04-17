from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_bcrypt import Bcrypt 
from flask import render_template,redirect,session,request,flash
from flask_app.models.models_user import User
from flask_app.models import models_user
from flask_app.models import models_car
from flask_app.controllers import controllers_cars
bcrypt = Bcrypt(app)
from flask import flash
import re
r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 



@app.route('/')
def loginreg():
    return render_template('loginreg.html')

@app.route('/register'  , methods = ['post'])
def register():
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email':request.form['email'],
        'password':pw_hash
    }
    
    user_in_db = User.get_by_email(data)
    if  user_in_db:
        flash("account already exist")
        return redirect("/")
    
    
    if not User.validate_user(request.form):
        flash ('') 
        return redirect('/')
    user_id = User.savetoregister(data)
    session['user_id'] = user_id
    return redirect ('/alltrips')


    

@app.route('/login' ,  methods = ['post'])
def login():
    if not User.validate_login(request.form):
        return redirect('/')
    # see if the email provided exists in the database
    data = { "email" : request.form["email"]}
    user_in_db = User.get_by_email_login(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    
    
    if not bcrypt.check_password_hash(user_in_db.password , request.form['password']):
        flash('invalid email/password')
        return redirect ('/')

    # if the passwords matched, we set the user_id into session
    # never render on a post!!!
    session['user_id'] = user_in_db.id
    return redirect ('/alltrips')






@app.route('/reset')
def logout():
    session.clear()
    return redirect('/')