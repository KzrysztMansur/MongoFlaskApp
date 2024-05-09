from flask import redirect, url_for, render_template, request
from . import app

tags = ["terror", "romance", "matemáticas", "shitpost", "física", "uwu", "derecho", "comercio", "quantica", "ciencia ficción"]

@app.route('/', methods=['GET','POST'])
@app.route('/inventory', methods=['GET','POST'])
def inventory():

    if request.method=='POST':
        # Handle POST Request here
        return render_template('inventory.html')        

    return render_template('inventory.html', tags=tags)         

@app.route('/create_tag', methods=['GET','POST'])
def create_tag():
    if request.method =='POST':

        tags.append(request.form['tagName'])
        #redirect(url_for('inventory'))

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

