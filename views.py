from flask import render_template, request, redirect, url_for, flash
from models import db, Car, Info

def init_routes(app):

    @app.route('/', methods=['GET'])
    def get_items():
        cars = Car.query.all()
        return render_template('index.html', message='Displaying all items', cars=cars)

    @app.route('/view/<id>', methods=['GET'])
    def view_item(id):
        car = Car.query.get(id)
        return render_template('view.html', car=car)

    @app.route('/car_image/<int:car_id>')
    def car_image(car_id):
        car = Car.query.get_or_404(car_id)
        if car.image:
            return car.image, 200, {"Content-Type": "image/jpeg"}
        return "No image", 404

    @app.route('/car/<int:car_id>/update', methods=['GET', 'POST'], endpoint='update_car')
    def update_car(car_id):
        car = Car.query.get_or_404(car_id)

        if request.method == 'POST':
            car.make = request.form['make']
            car.model = request.form['model']
            car.color = request.form['color']
            car.horsepower = request.form['horsepower']
            car.year = request.form['year']
            car.odometer = request.form['odometer']

            db.session.commit()
            return redirect(url_for('get_items', id=car.id))

        return render_template('edit.html', car=car)

    @app.route('/delete', methods=['POST'])
    def delete_item():
        car_id = request.form['id']
        car = Car.query.get(car_id)
        db.session.delete(car)
        db.session.commit()
        return redirect(url_for('get_items'))

    @app.route('/signup', methods=['GET', 'POST'])
    def sign_up():
            if request.method == 'POST':            
                new_user = Info(
                    email = request.form.get('email'),
                    password = request.form.get('password')
                )
            
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('get_items'))
            return render_template('signup.html')


            
    
            #return redirect(url_for('get_items'))
         #return render_template('signup.html')

    @app.route('/add', methods=['POST', 'GET'])
    def create_item():
        if request.method == 'POST':
            file = request.files.get('image')
            image_data = None
            filename = None

            if file:
                image_data = file.read()
                filename = file.filename

            new_car = Car(
                make=request.form['make'],
                model=request.form['model'],
                color=request.form['color'],
                horsepower=int(request.form['horsepower']),
                year=int(request.form['year']),
                odometer=int(request.form['odometer']),
                image=image_data,
                filename=filename
            )
            db.session.add(new_car)
            db.session.commit()
            return redirect(url_for('get_items'))

        return render_template('add.html', message='Item added successfully')
    
    @app.route('/login', methods=['POST', 'GET'])
    def Log_in():
        if request.method == 'GET':
            return render_template('login.html')
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            user = Info.query.filter_by(email=email, password=password).first()
            if user:
                print("SUCCESS!")  
                return redirect(url_for('get_items')) 
            else:
                print("INVALID CREDENTIALS")
                return render_template('login.html', error="Invalid email or password")


        
        return redirect(url_for('get_items'))

    @app.route('/search', methods=['GET'])
    def search_items():
        search_query = request.args.get('query', ' ')
        search_query = search_query.strip().lower()
        if search_query:
            items = Car.query.filter(Car.make.ilike(f'%{search_query}%')).all()
        else:
            items = Car.query.all()

        return render_template('search.html', items=items)

