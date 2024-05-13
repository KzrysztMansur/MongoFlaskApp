from . import app, mongo_client
from .model import TagManager, ProductManager
from flask import redirect, url_for, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
import os


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class Product:
    def __init__(self, img, name, price, description, tags):
        self.img = "pink donut.jpg"
        self.name = name
        self.price = price
        self.description = description
        self.tags = tags

class Tag:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        
tag_manager = TagManager(mongo_client['book_store'])

tags = tag_manager.get_all_tags()
print(tags)

product_manager = ProductManager(mongo_client['book_store'])
products = product_manager.get_all_products()

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.join(app.root_path, 'static'), filename)

@app.route('/', methods=['GET', 'POST'])
@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    tag_manager = TagManager(mongo_client['book_store'])
    tags = tag_manager.get_all_tags()

    product_manager = ProductManager(mongo_client['book_store'])
    products = product_manager.get_all_products()
    if request.method == 'POST':
        # Handle POST Request here
        return render_template('inventory.html')

    return render_template('inventory.html', tags=tags, products=products, tag_manager=tag_manager, str=str)


@app.route('/create_tag', methods=['GET', 'POST'])
def create_tag():
    if request.method == 'POST':
        
        #count = len(tags)
        #tags.append(Tag(count, request.form['tagName']))
        tag_manager.add_tag(request.form['tagName'].capitalize())
        return redirect(url_for('inventory'))

    return render_template('inventory.html', tags=tags)


@app.route('/update_tag/<string:tag_id>', methods=['GET', 'POST'])
def update_tag(tag_id):
    if request.method == 'POST':
        new_tag_name = request.form.get('newTagName')
        if new_tag_name:
            # Update the tag in the database
            # Assuming you have a TagManager class with a method update_tag_name
            tag_manager.update_tag(tag_id, new_tag_name)
        return redirect(url_for('inventory'))

    return render_template('inventory.html', tags=tags, products=products)


@app.route('/delete_tag/<string:tag_index>', methods=['GET', 'POST'])
def delete_tag(tag_index):
    if request.method == 'POST':
        tag_id = request.form.get('tag_id')
        if tag_id is not None:
            try:
                # se borra de la base de datos
                tag_manager.delete_tag(tag_id)
                # no se pudo borrar
            except Exception:
                # Handle the case where the index is out of range
                print("unknown exception")
                pass

            return redirect(url_for('inventory'))

    return render_template('inventory.html', tags=tags, products=products)


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        file = request.files['product_img']
        upload_folder = app.config['UPLOAD_FOLDER']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)

            name = request.form['name']
            price = float(request.form['price'])
            description = request.form['description']
            selected_tags = request.form.getlist('tags[]')

            selected_tags = [str(tag) for tag in selected_tags]
  

            product_manager.add_product(name, price, description, image_url=filename, tags=selected_tags)

        return redirect(url_for('inventory'))

    return render_template('inventory.html', tags=tags)


@app.route('/delete_product/<string:product_id>', methods=['POST'])
def delete_product(product_id):
    
    if request.method == 'POST':
        
        product_manager.delete_product(product_id)

    return redirect(url_for('inventory'))



# DESDE AQUÍ SE EMPIEZA A VER LA VISTA DEL COMPRADOR
@app.route('/customer_view', methods=['GET', 'POST'])
def customer_view():
    
    if request.method == 'POST':


        return redirect(url_for('process_selected_tags'))

    selected_products = products
    return render_template('customer_view.html', tags=tags, products=selected_products)

@app.route('/process_selected_tags', methods=['POST'])
def process_selected_tags():
    selected_tags = request.form.getlist('selectedTags')
    if not selected_tags:
        # If no tags selected, return all products
        return redirect(url_for('customer_view'))
    else:
        # Find products by selected tags
        selected_products = product_manager.find_products_by_tags(selected_tags)
        return render_template('customer_view.html', tags=tags, products=selected_products)
