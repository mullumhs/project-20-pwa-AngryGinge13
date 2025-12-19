from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String)
    model = db.Column(db.String)
    color = db.Column(db.String)
    horsepower = db.Column(db.String)
    year = db.Column(db.Integer)
    odometer = db.Column(db.Integer)
    engine = db.Column(db.String)
    image = db.Column(db.LargeBinary)
    filename = db.Column(db.String(100))
    
class Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    

    def __repr__(self):
        return f'<Task {self.title}>'
    



