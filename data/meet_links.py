import mongoengine 

class AnimalImages(mongoengine.Document):
    name = mongoengine.StringField()
    species = mongoengine.StringField()