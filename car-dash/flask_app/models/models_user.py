from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
db = 'cardash_schema'
r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__ (self , data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        
    @classmethod
    def get_by_email(cls , data):
        query = 'select * from users where email = %(email)s'
        results = connectToMySQL(db).query_db(query ,  data)
        return results
    
    @classmethod
    def get_by_email_login(cls , data):
        query = 'select * from users where email = %(email)s'
        results = connectToMySQL(db).query_db(query ,  data)
        return cls(results[0])
        
    @classmethod
    def savetoregister(cls , data):
        query = 'insert into users (first_name , last_name , email , password ) values ( %(first_name)s  ,  %(last_name)s  , %(email)s , %(password)s  )'
        return  connectToMySQL(db).query_db(query , data)
    
    
    @staticmethod
    def validate_user(users):
        is_valid = True
        if len(users['first_name']) < 2 or len(users['first_name']) > 21 :
            flash("first_name must be between 1 and 21  characters.")
            is_valid = False
        if not EMAIL_REGEX.match(users['email']):
            flash('Invalid Email.')
            is_valid = False
        if len(users['password']) < 1:
            flash("Please enter a password")
            is_valid = False
        return is_valid
    
    
    @staticmethod
    def validate_login(data):
        is_valid = True
        #check email format
        if not EMAIL_REGEX.match(data['email']):
            flash('Invalid Email', 'login')
            is_valid = False
            return is_valid
        #check password for required length, number included, capital included
        if not len(data['password']) > 7 or re.search('[0-9]', data['password']) is None or re.search('[A-Z]', data['password']) is None:
            flash('Password must contain at least 8 characters, a number, and a capital letter.', 'login')
            is_valid = False
        return is_valid
    
    
