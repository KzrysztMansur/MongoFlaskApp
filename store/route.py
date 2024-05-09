from flask import redirect, url_for, render_template, request
from . import app
                        
@app.route('/', methods=['GET','POST'])
def inventory_tags():
    tags = ["terror", "romance", "matemáticas", "shitpost", "física", "uwu"]
    if request.method=='POST':
        # Handle POST Request here
        return render_template('inventory.html')        

    return render_template('inventory.html', tags=tags)         





@app.route('/', methods=['GET', 'POST'])
def costumer_view():
    tags = []
    if request.method=='POST':
        #aquí lo logica para que solamente regrese solo los objetos de los tags seleccionados
        products = []

        return render_template('costumerview.html', tags=tags, products=products)
    
    #aquí es para que regrese los objetos sin ningun tipo de filtro
    products = []

    return render_template('costumerview.html', tags=tags, products=products)

