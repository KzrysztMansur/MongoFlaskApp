from typing import List, Dict, Any, Optional
from bson import ObjectId


class TagManager:
    def __init__(self, db):
        """
        Initialize the TagManager with a MongoDB database.

        :param db: MongoDB database instance
        """
        self.collection = db['tags']

    def add_tag(self, name: str):
        """
        Add a new tag to the database.

        :param name: The name of the tag to add
        """
        self.collection.insert_one({'name': name})

    def get_tag_by_id(self, tag_id: str) -> Dict[str, Any]:
        """
        Retrieve a tag by its ID.

        :param tag_id: The ID of the tag to retrieve
        :return: The retrieved tag document
        """
        return self.collection.find_one({'_id': ObjectId(tag_id)})

    def get_all_tags(self) -> List[Dict[str, Any]]:
        """
        Retrieve all tags from the database.

        :return: A list of all tag documents
        """
        return list(self.collection.find({}))

    def update_tag(self, tag_id: str, new_name: str) -> Optional[bool]:
        """
        Update the name of an existing tag.

        :param tag_id: The ID of the tag to update
        :param new_name: The new name for the tag
        :return: True if the update was successful, None otherwise
        """
        return self.collection.update_one({'_id': ObjectId(tag_id)}, {'$set': {'name': new_name}}).modified_count

    def delete_tag(self, tag_id: str) -> Optional[bool]:
        """
        Delete a tag by its ID.

        :param tag_id: The ID of the tag to delete
        :return: True if the deletion was successful, None otherwise
        """
        return self.collection.delete_one({'_id': ObjectId(tag_id)}).deleted_count


class ProductManager:
    def __init__(self, db):
        """
        Initialize the ProductManager with a MongoDB database instance.

        :param db: MongoDB database instance
        """
        self.collection = db['products']

    def add_product(self, name: str, price: float, description: str, image_url: str,
                    tags: Optional[List[str]] = None):
        """
        Add a new product to the database.

        :param name: The name of the product
        :param price: The price of the product
        :param description: The description of the product
        :param image_url: The URL of the product image
        :param tags: Optional; List of tag IDs associated with the product. Can be an empty list.
        :return: The ID of the created product
        """
        self.collection.insert_one({
            'name': name,
            'price': price,
            'description': description,
            'image_url': image_url,
            'tags': [ObjectId(tag) for tag in tags] if tags else []
        })

    def get_product_by_id(self, product_id: str) -> Dict[str, Any]:
        """
        Retrieve a product by its ID.

        :param product_id: The ID of the product to retrieve
        :return: The retrieved product document
        """
        return self.collection.find_one({'_id': ObjectId(product_id)})

    def get_all_products(self) -> List[Dict[str, Any]]:
        """
        Retrieve all products from the database.

        :return: A list of all product documents
        """
        return list(self.collection.find({}))

    def update_product(self, product_id: str, name: Optional[str] = None, price: Optional[float] = None,
                       description: Optional[str] = None, image_url: Optional[str] = None,
                       tags: Optional[List[str]] = None) -> Optional[bool]:
        """
        Update the information of an existing product.

        :param product_id: The ID of the product to update
        :param name: Optional; The new name of the product
        :param price: Optional; The new price of the product
        :param description: Optional; The new description of the product
        :param image_url: Optional; The new image URL of the product
        :param tags: Optional; The new list of tag IDs for the product
        :return: True if the update was successful, None otherwise
        """
        update_data = {k: v for k, v in locals().items() if v is not None and k != 'product_id'}
        if 'tags' in update_data:
            update_data['tags'] = [ObjectId(tag) for tag in tags]
        return self.collection.update_one({'_id': ObjectId(product_id)}, {'$set': update_data}).modified_count

    def delete_product(self, product_id: str) -> Optional[bool]:
        """
        Delete a product by its ID.

        :param product_id: The ID of the product to delete
        :return: True if the deletion was successful, None otherwise
        """
        return self.collection.delete_one({'_id': ObjectId(product_id)}).deleted_count

    def find_products_by_tag(self, tag_id: str) -> List[Dict[str, Any]]:
        """
        Find all products that contain a specific tag.

        :param tag_id: The ID of the tag to search by
        :return: A list of products that contain the specified tag
        """
        return list(self.collection.find({'tags': ObjectId(tag_id)}))

    def find_products_by_tags(self, tags: List[str], match_all: bool = False) -> List[Dict[str, Any]]:
        """
        Find products based on a list of tags.

        :param tags: List of tag IDs to search by
        :param match_all: True to require all tags in each product, False to require at least one tag
        :return: A list of products that match the tag criteria
        """
        tags = [ObjectId(tag) for tag in tags]
        if match_all:
            query = {'tags': {'$all': tags}}
        else:
            query = {'tags': {'$in': tags}}
        return list(self.collection.find(query))
