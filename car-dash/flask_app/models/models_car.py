from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import models_user
from flask_app.models.models_user import User


db = 'cardash_schema'


class Car:
    def __init__ (self , data):
        self.id = data['id']
        self.name = data['name']
        self.liscenseplate_number = data['liscenseplate_number']
        self.color = data['color']
        self.model = data['model']
        self.leavetime = data['leavetime']
        self.arrivaltime = data['arrivaltime']
        self.user_id = data['user_id']
        
        #initiation and build of the car class
        
        
    @classmethod
    def getall(cls):
        query = """Select * from cars
        join users on users.id = cars.user_id
        """
        
        # run the query above which will gather every car in the  database for the cars table
        results = connectToMySQL(db).query_db(query)
        #set the variable results to connect to the database (db) otherwise known as cardash_schema from lne 6 and run the function query_db from the mysqlconnection file and pass in the prementiond query
        users = []
        #set variable cars to an emtey list 
        for user in results: 
            driver = cls(user)
            user_data = {
            'id':user['id'],
            'first_name':user['first_name'],
            'last_name':user['last_name'],
            'email':user['email'],
            'password':user['password']
            }
            #for every (placeholder name in this case user) in the database 
            driver.rider = User(user_data)
            users.append(driver)
            #list.append but since results is not created as a list we use users and say users.append (whatever the placeholder is in this case)user
        return users
        #return the list of users
        #and the join will get the cars
    
    @classmethod
    def createtrip(cls , data):
        query = """insert into cars ( name , liscenseplate_number , color , model   , user_id , leavetime , arrivaltime ) values
        (   %(name)s , %(liscenseplate_number)s , %(color)s , %(model)s  , %(user_id)s , Now() , Now() )
        """
        #insert into the cars table the values into the rows above 
        return connectToMySQL(db).query_db(query , data)
    #return the database with the query that was ran and all of the new data
    
    @classmethod
    def selecttoedit(cls , data):
        query = 'select * from cars where id = %(id)s'
        #select every car where the car has a specific id (which is what makes the cars uniqe)
        results = connectToMySQL(db).query_db(query, data)
        cars = []
        #we are using the cars list because cars is what we awant to loop through
        #no join because we are focused on the car and the name much like in dooordash will tell us everything we need to know
        for car in results:
            cars.append(car)
        return cars
    
    
    @classmethod
    def updatetrip(cls , data):
        query = 'update cars set name = %(name)s  , liscenseplate_number =  %(liscenseplate_number)s , color = %(color)s , model = %(model)s  where id = %(id)s'
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def delete(cls , data):
        query = 'Delete from cars where id = %(id)s'
        return connectToMySQL(db).query_db(query , data)

                
            
