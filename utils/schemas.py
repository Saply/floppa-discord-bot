from mongoengine import *
import mongoengine.errors as e

class ClassDetails(EmbeddedDocument):
    class_name = StringField()
    class_group = StringField()
    duration = IntField()

    link = URLField()
    lecturer_name = StringField()
    ImageField

    meta = {
        'strict': False
    }
    

class ClassCollection(Document):
    class_id = SequenceField()
    channel_id = LongField()
    guild_id = LongField()

    date_time = DateTimeField()
    repeatable = BooleanField()

    notify = ListField(LongField())

    class_details = EmbeddedDocumentField(ClassDetails)

    
    meta = {
        'collection': 'class_collection',
        'strict': False
    }
    

