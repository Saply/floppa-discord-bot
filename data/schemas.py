from mongoengine import *
import mongoengine.errors as e

class ClassDetails(EmbeddedDocument):
    class_name = StringField()
    class_group = StringField()
    duration = IntField()

    link = URLField()
    lecturer_name = StringField()

    meta = {
        'strict': False
    }
    

class ClassCollection(Document):
    class_id = SequenceField()
    channel_id = LongField()

    date_time = DateTimeField()
    repeatable = BooleanField()

    # Users to ping when there's a class
    notify = ListField(LongField())

    class_details = EmbeddedDocumentField(ClassDetails)
    
    # do meta indexing for link and start time 
    # https://mongoengine-odm.readthedocs.io/apireference.html#mongoengine.Document
    # https://mongoengine-odm.readthedocs.io/apireference.html#mongoengine.FieldDoesNotExist
    
    
    meta = {
        'collection': 'class_collection',
        'strict': False
    }
    

