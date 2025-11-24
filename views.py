from flask import render_template, request, redirect, url_for, flash
from models import db, Car



# Define your routes inside the 'init_routes' function
# Feel free to rename the routes and functions as you see fit
# You may need to use multiple methods such as POST and GET for each route
# You can use render_template or redirect as appropriate
# You can also use flash for displaying status messages

def init_routes(app):

    @app.route('/', methods=['GET'])
    def get_items():
        cars = Car.query.all()
        return render_template('index.html', message='Displaying all items', cars = cars)
    
    @app.route('/view/<id>', methods=['GET'])
    def update_item(id):
        car = Car.query.get(id)
        return render_template('view.html', car = car)




    @app.route('/car_image/<int:car_id>')
    def car_image(car_id):
        car = Car.query.get_or_404(car_id)
        if car.image:
            return car.image, 200, {"Content-Type": "image/jpeg"}
        return "No image", 404



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

    #@app.route('/update', method=['POST'])
   # def veiw_item():
       # return render_template('index.html', message=f'Item updated successfully')
    


    @app.route('/delete', methods=['POST'])
    def delete_item():
        
        car_id = request.form['id']
        car = Car.query.get(id)

        db.session.delete(car)
        db.session.commit()
        return render_template('index.html', message=f'Item deleted successfully')