from mongoengine import *
import mongoengine.errors as e
import datetime as dt

class ClassDetails(EmbeddedDocument):
    class_name = StringField()
    class_group = StringField()
    duration = IntField()

    day = StringField()
    start_time = IntField()

    link = URLField()
    lecturer_name = StringField()

    meta = {
        'strict': False
    }
    

class ClassCollection(Document):
    id = SequenceField()

    # probably not needed?
    roles_editable = ListField(LongField()) # default = roles array of current user as well as any role higher permed than it
    # DiscordUtility.rolesGetter
    channel_id = LongField() # default = current channel

    dates = DateTimeField()
    repeatable = BooleanField()
    class_details = EmbeddedDocumentField(ClassDetails)
    
    # do meta indexing for link and start time 
    # https://mongoengine-odm.readthedocs.io/apireference.html#mongoengine.Document
    # https://mongoengine-odm.readthedocs.io/apireference.html#mongoengine.FieldDoesNotExist
    
    
    meta = {
        'strict': False
    }
    

