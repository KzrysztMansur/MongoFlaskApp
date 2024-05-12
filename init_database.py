from pymongo import MongoClient
from bson import ObjectId


def main():
    client = MongoClient('localhost', 27017)

    # Verificar si la base de datos existe
    if 'book_store' in client.list_database_names():
        print("Database already exists.")
        return

    db = client['book_store']

    # Crear colecciones si no existen
    tags_collection = db['tags']
    products_collection = db['products']

    # Crear un índice en el campo 'name' de la colección 'tags'
    tags_collection.create_index('name', unique=True)

    # Comprobar si las colecciones están vacías
    if tags_collection.count_documents({}) == 0 and products_collection.count_documents({}) == 0:
        # Agregar tags de ejemplo
        tags_info = [
            {'name': 'Literature'},
            {'name': 'Science'},
            {'name': 'Fiction'},
            {'name': 'Non-Fiction'},
            {'name': 'Biography'},
            {'name': "Children's Books"}
        ]
        tags_ids = [tags_collection.insert_one(tag).inserted_id for tag in tags_info]

        # Agregar productos de ejemplo
        products_info = [
            {
                'name': '1984',
                'price': 9.99,
                'description': 'A dystopian novel by George Orwell.',
                'image_url': '1984.jpg',
                'tags': [tags_ids[0]]
            },
            {
                'name': 'A Brief History of Time',
                'price': 15.99,
                'description': 'A popular-science book on cosmology by Stephen Hawking.',
                'image_url': 'a_brief_history_of_time.jpg',
                'tags': [tags_ids[1]]
            },
            {
                'name': 'To Kill a Mockingbird',
                'price': 8.99,
                'description': 'A novel by Harper Lee, dealing with racial inequality.',
                'image_url': 'to_kill_a_mockingbird.jpg',
                'tags': [tags_ids[2], tags_ids[0]]
            },
            {
                'name': 'The Selfish Gene',
                'price': 12.99,
                'description': 'A book on evolution by Richard Dawkins, introducing the concept of the "selfish gene".',
                'image_url': 'the_selfish_gene.jpg',
                'tags': [tags_ids[1], tags_ids[3]]
            },
            {
                'name': 'Steve Jobs',
                'price': 18.99,
                'description': 'Biography of Steve Jobs by Walter Isaacson.',
                'image_url': 'steve_jobs.jpg',
                'tags': [tags_ids[4]]
            },
            {
                'name': 'Harry Potter and the Sorcerer\'s Stone',
                'price': 10.99,
                'description': 'The first book in J.K. Rowling\'s Harry Potter series.',
                'image_url': 'harry_potter_and_the_sorcerers_stone.jpg',
                'tags': [tags_ids[5], tags_ids[2]]
            }
        ]
        for product in products_info:
            products_collection.insert_one(product)

        print("Database and collections created with initial data.")
    else:
        print("Database and collections already have data.")

    # Imprimir los datos de ejemplo para verificar
    print("Current data in the 'tags' collection:")
    for tag in tags_collection.find():
        print(tag)
    print("Current data in the 'products' collection:")
    for product in products_collection.find():
        print(product)


if __name__ == '__main__':
    main()
