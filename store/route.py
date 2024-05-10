from flask import redirect, url_for, render_template, request
from werkzeug.utils import secure_filename
import os
from . import app

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Define the allowed file extensions


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class Card:
    def __init__(self, img, name, price, description, tags_id):
        self.img = img
        self.name = name
        self.price = price
        self.description = description
        self.tags_id = tags_id

tags = ["terror", "romance", "matemáticas", "shitpost", "física", "uwu", "derecho", "comercio", "quantica", "ciencia ficción"]
cards = [Card(None, "maths for dummies", 70, "this is a book for people who dont know maths", [2, 3, 4, 5]),
         Card(None, "php for dummies", 70, "this is a book for people who dont know php", [2, 3, 4, 5]),
         Card(None, "web for dummies", 70, "this is a book for people who dont know web", [2, 3, 4, 5])
         ]


@app.route('/', methods=['GET','POST'])
@app.route('/inventory', methods=['GET','POST'])
def inventory():

    if request.method=='POST':
        # Handle POST Request here
        return render_template('inventory.html')        

    return render_template('inventory.html', tags=tags, cards=cards)         

@app.route('/create_tag', methods=['GET','POST'])
def create_tag():
    if request.method =='POST':

        tags.append(request.form['tagName'])
        return redirect(url_for('inventory'))

    return render_template('inventory.html', tags=tags)

@app.route('/add_product', methods=['GET','POST'])
def add_product():
    if request.method =='POST':
        #file = request.files['productImage']
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        selected_tags = request.form.getlist('tags[]')

        print(name)
        print(price)
        print(description)
        print(selected_tags)


        return redirect(url_for('inventory'))

    return render_template('inventory.html', tags=tags)



@app.route('/costumer_view', methods=['GET', 'POST'])
def costumer_view():
    tags = []
    if request.method=='POST':
        #aquí lo logica para que solamente regrese solo los objetos de los tags seleccionados
        products = []

        return render_template('costumerview.html', tags=tags, products=products)
    
    #aquí es para que regrese los objetos sin ningun tipo de filtro
    products = []

    return render_template('costumerview.html', tags=tags, products=products)

