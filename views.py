#imports
from flask import render_template, request, redirect, url_for, flash
from models import db, Car, Info
from sqlalchemy import or_, cast, String
#intialize routes
def init_routes(app):

    @app.route('/', methods=['GET'])
    def get_items():
        # Retrieve all items from the database
        cars = Car.query.all()
        return render_template('index.html', message='Displaying all items', cars=cars)
    # View a single item
    @app.route('/view/<id>', methods=['GET'])
    def view_item(id):
        # Retrieve the item by ID
        car = Car.query.get(id)
        return render_template('view.html', car=car)
    # Serve car image
    @app.route('/car_image/<int:car_id>')
    # Serve car image
    def car_image(car_id):
        car = Car.query.get_or_404(car_id)
        # Return the image data with appropriate headers
        if car.image:
            return car.image, 200, {"Content-Type": "image/jpeg"}
        # If no image is found, return a default response or placeholder
        return "No image", 404
    # Update an existing item
    @app.route('/car/<int:car_id>/update', methods=['GET', 'POST'], endpoint='update_car')
    def update_car(car_id):
        # Retrieve the item by ID
        car = Car.query.get_or_404(car_id)
        # Handle form submission
        if request.method == 'POST':
            car.make = request.form['make']
            car.model = request.form['model']
            car.color = request.form['color']
            car.horsepower = request.form['horsepower']
            car.year = request.form['year']
            car.odometer = request.form['odometer']
            
            file = request.files.get('image')
            # Update image if a new file is provided
            if file and file.filename != "":
                car.image = file.read()
                car.filename = file.filename
            # Commit the changes to the database
            db.session.commit()
            return redirect(url_for('get_items'))
        # Render the edit form with existing item data
        return render_template('edit.html', car=car)
    # Delete an item
    @app.route('/delete', methods=['POST'])
    def delete_item():  
        # Get the item ID from the form
        car_id = request.form['id']
        car = Car.query.get(car_id)
        db.session.delete(car)
        db.session.commit()
        return redirect(url_for('get_items'))
    # Sign Up route
    @app.route('/signup', methods=['GET', 'POST'])
    def sign_up(): 
        # Handle GET request
        if request.method == 'GET':
            return render_template('signup.html')
        # Handle POST request
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            # First check: empty fields
            if not email or not password:
                print("EMPTY FIELDS")
                return render_template('signup.html', error="Please enter both email and password")
            # Second check: existing user
            new_user = Info(
                email=email,
                password=password
            )
            db.session.add(new_user)
            db.session.commit()
            
            print("USER CREATED SUCCESSFULLY")
            return redirect(url_for('get_items'))
    # Add a new car
    @app.route("/add", methods=["GET", "POST"])
    def add_car():
        # Handle form submission
        if request.method == "POST":

            make = request.form.get("make")
            model = request.form.get("model")
            color = request.form.get("color")
            engine = request.form.get("engine")

            horsepower = request.form.get("horsepower")
            horsepower = int(horsepower) if horsepower else None

            year = int(request.form.get("year"))        # required
            odometer = int(request.form.get("odometer"))  # required
            # Handle image upload
            image = request.files.get("image")
            image_data = None
            filename = None
        
            if image and image.filename != "":
                filename = image.filename
                image_data = image.read()
            # Create a new Car object
            car = Car(
                make=make,
                model=model,
                color=color,
                horsepower=horsepower,
                year=year,
                odometer=odometer,
                engine=engine,
                image=image_data,
                filename=filename
            )

            db.session.add(car)
            db.session.commit()

            return redirect(url_for("get_items"))

        return render_template("add.html")
    # Log In route
    @app.route('/login', methods=['POST', 'GET'])
    def Log_in():

        if request.method == 'GET':
            return render_template('login.html')
        
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            # First check: empty fields
            if not email or not password:
                print("EMPTY FIELDS")
                return render_template('login.html', error="Please enter both email and password")

            # Then check: valid user
            user = Info.query.filter_by(email=email, password=password).first()
            if user:
                print("SUCCESS!")  
                return redirect(url_for('get_items'))
            else:
                print("INVALID CREDENTIALS")
                return render_template('login.html', error="Invalid email or password")
    # Search items
    @app.route('/search', methods=['GET'])
    def search_items():
        query = request.args.get("query", "")
        year = request.args.get("year")
        make = request.args.get("make")

        cars = Car.query

        if query:
            cars = cars.filter(
                or_(
                    Car.make.ilike(f"%{query}%"),
                    Car.model.ilike(f"%{query}%"),
                    Car.color.ilike(f"%{query}%"),
                    Car.engine.ilike(f"%{query}%"),
                    Car.year.cast(db.String).ilike(f"%{query}%"),
                    Car.odometer.cast(db.String).ilike(f"%{query}%")
                )
            )

        if year:
            cars = cars.filter(Car.year == year)

        if make:
            cars = cars.filter(Car.make.ilike(f"%{make}%"))

        cars = cars.order_by(Car.year.desc()).all()

        return render_template("search.html", items=cars)
