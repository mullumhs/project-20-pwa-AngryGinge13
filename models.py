from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.db'
db = SQLAlchemy(app)



class Cars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String)
    model = db.Column(db.String)
    color = db.Column(db.String)
    year = db.Column(db.Integer)
    odometer = db.Column(db.Integer)
    

    def __repr__(self):
        return f'<Task {self.title}>'
    
@app.route('/add', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        new_car = Cars(
            make=request.form['make'],
            model=request.form['model'],
            color=request.form['color'],
            year=int(request.form['year']),
            odometer=int(request.form['odometer'])
        )
        db.session.add(new_car)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')


