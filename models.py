from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.db'
db = SQLAlchemy(app)



class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String)
    model = db.Column(db.String)
    color = db.Column(db.String)
    horsepower = db.Column(db.String)
    year = db.Column(db.Integer)
    odometer = db.Column(db.Integer)
    image = db.Column(db.LargeBinary)
    filename = db.Column(db.String(100))
    

    def __repr__(self):
        return f'<Task {self.title}>'
    



