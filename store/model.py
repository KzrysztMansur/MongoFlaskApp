from store import mongo

class Product:
    def __init__(self, name, description, image_url, tags):
        self.name = name
        self.description = description
        self.image_url = image_url
        self.tags = tags

    @staticmethod
    def get_by_name(name):
        return mongo.db.users.find_one({'name': name})
    
    @staticmethod
    def get_by_tags(tags):
        return mongo.db.products.find({'tags.id': {'$in': tags}})


    def save(self):
        mongo.db.users.insert_one({
            'name': self.name,
            'description': self.description,
            'image_url': self.image_url
        })

    
    def add_tags(self, new_tags):
        if isinstance(new_tags, list):
            self.tags.extend(new_tags)
        else:
            self.tags.append(new_tags)

        mongo.db.products.update_one({'_id': self.id}, {'$set': {'tags': self.tags}})



class Tags:
    def __init__(self, id, tag):
        self.id = id
        self.tag = tag

    @staticmethod
    def get_tags_by_product(user_id):
        return mongo.db.posts.find({'id': user_id})
    
 
    def update_tag_name(self, old_tag_name, new_tag_name):

        mongo.db.tags.update_one({'id': self.id, 'tag': old_tag_name}, {'$set': {'tag': new_tag_name}})
        self.tag = new_tag_name  


    def save(self):
        mongo.db.posts.insert_one({
            'title': self.id,
            'content': self.tag,
        })
                