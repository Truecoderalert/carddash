from flask_app.config.mysqlconnection import connectToMySQL
from flask import render_template,redirect,session,request,flash
from flask_app import app
from flask_app.models.models_car import Car
from flask_app.models  import models_car
from flask_app.models import models_user

@app.route('/alltrips')
def showalltrips():
    trips = Car.getall()
    #the variable trips is short for the enter the class and execute the function of getall which will get all entries in the table from the query most likely in the function
    return render_template ('alltrips.html' , trips = trips)

@app.route('/createtrip' )
def createtrip():
    return render_template('createres.html')

@app.route('/verify'  , methods = ['post'])
def verifytrip():
    data = {'name' :request.form['name'] , 
            'liscenseplate_number':request.form['liscenseplate_number'],
            'color':request.form['color'],
            'model':request.form['model'],
            'user_id':request.form['user_id']
            }
    Car.createtrip(data)
    return redirect ('/alltrips')

@app.route('/editcar/<int:id>')
def editcar(id):
    data = {'id':id}
    #data is id passed as id when the car class is initiated on line 11 in  the models
    #user_id is declared in the class so their is no confusion
    car = Car.selecttoedit(data)
    return render_template ('editcar.html' , car = car)

@app.route('/view/vehicle/<int:id>')
def viewcar(id):
    data = {'id':id}
    car = Car.selecttoedit(data)
    return render_template('viewvehicle.html' ,  car = car)

@app.route('/re_verify/<int:id>' , methods=['post'])
def update(id):
    data = {'name' :request.form['name'] , 
            'liscenseplate_number':request.form['liscenseplate_number'],
            'color':request.form['color'],
            'model':request.form['model'],
            'id':request.form['id']}
    Car.updatetrip(data)
    return redirect ('/alltrips')

@app.route('/delete/<int:id>')
def delete(id):
    data = {'id':id}
    Car.delete(data)
    return redirect ('/alltrips')