from . import app
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
        

tags = [
    Tag(0, "terror"),
    Tag(1, "romance"),
    Tag(2, "matemáticas"),
    Tag(3, "shitpost"),
    Tag(4, "física"),
    Tag(5, "uwu"),
    Tag(6, "derecho"),
    Tag(7, "comercio"),
    Tag(8, "quantica"),
    Tag(9, "ciencia ficción")
]

cards = [Product("MongoFlaskApp\store\static\img_urls\pink donut.jpg", "maths for dummies", 70, "this is a book for people who dont know maths", [tags[2], tags[3], tags[4], tags[5]]),
         Product("MongoFlaskApp\store\static\img_urls\pink donut.jpg", "php for dummies", 70, "this is a book for people who dont know php", [tags[2], tags[3], tags[4], tags[5]]),
         Product("MongoFlaskApp\store\static\img_urls\pink donut.jpg", "web for dummies", 70, "this is a book for people who dont know web", [tags[2], tags[3], tags[4], tags[5]])
         ]


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.join(app.root_path, 'static'), filename)

@app.route('/', methods=['GET', 'POST'])
@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    if request.method == 'POST':
        # Handle POST Request here
        return render_template('inventory.html')

    return render_template('inventory.html', tags=tags, cards=cards)


@app.route('/create_tag', methods=['GET', 'POST'])
def create_tag():
    if request.method == 'POST':
        count = len(tags)
        tags.append(Tag(count, request.form['tagName']))
        return redirect(url_for('inventory'))

    return render_template('inventory.html', tags=tags)


@app.route('/update_tag/<int:tag_index>', methods=['GET', 'POST'])
def update_tag(tag_index):
    if request.method == 'POST':
        new_tag_name = request.form.get('newTagName')
        if new_tag_name:
            # Update the name attribute of the Tag instance
            tags[tag_index].name = new_tag_name
        return redirect(url_for('inventory'))

    return render_template('inventory.html', tags=tags, cards=cards)


@app.route('/delete_tag/<int:tag_index>', methods=['GET', 'POST'])
def delete_tag(tag_index):
    if request.method == 'POST':
        tag_id = int(request.form.get('tag_id'))
        if tag_id is not None:
            try:
                # If you're using a list to store tags
                tags.pop(tag_index)
                # If you're using a database, you would perform a deletion operation here
            except IndexError:
                # Handle the case where the index is out of range
                pass

            return redirect(url_for('inventory'))

    return render_template('inventory.html', tags=tags, cards=cards)


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        file = request.files['product_img']
        upload_folder = app.config['UPLOAD_FOLDER']

        # Ensure the upload folder exists
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)

            name = request.form['name']
            price = request.form['price']
            description = request.form['description']
            selected_tags = request.form.getlist('tags[]')

            print(name)
            print(price)
            print(description)
            for tag in selected_tags:
                print(tag)
            print('File saved as:', filename)

        return redirect(url_for('inventory'))

    return render_template('inventory.html', tags=tags)


# DESDE AQUÍ SE EMPIEZA A VER LA VISTA DEL COMPRADOR
@app.route('/customer_view', methods=['GET', 'POST'])
def customer_view():
    if request.method == 'POST':
        # aquí lo logica para que solamente regrese solo los objetos de los tags seleccionados
        # products = []

        return render_template('customer_view.html', tags=tags, cards=cards)

    # aquí es para que regrese los objetos sin ningun tipo de filtro
    # products = [] 

    return render_template('customer_view.html', tags=tags, cards=cards)

@app.route('/process_selected_tags', methods=['POST'])
def process_selected_tags():
    selected_tags = request.form.getlist('selectedTags')
    
    print('Selected tags received:', selected_tags)
    return redirect(url_for('customer_view'))

