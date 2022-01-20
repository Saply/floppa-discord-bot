from mongoengine import *
import mongoengine.errors as e
import datetime as dt


class ClassDetails(EmbeddedDocument):
    class_name = StringField()
    class_group = StringField()
    duration = IntField()
    start_time = IntField()

    link = URLField()
    lecturer_name = StringField()
    repeatable = BooleanField()

class ClassCollection(Document):
    id = SequenceField()
    roles_editable = ListField(LongField()) # default = roles array of current user as well as any role higher permed than it
    # DiscordUtility.rolesGetter
    channel_id = LongField() # default = current channel
    # date = DateTimeField(default = datetime.datetime.now)
    dates = DateTimeField(default = dt.datetime.now)
    class_details = EmbeddedDocumentField(ClassDetails)
    
    # do meta indexing for link and start time 
    # https://mongoengine-odm.readthedocs.io/apireference.html#mongoengine.Document
    # https://mongoengine-odm.readthedocs.io/apireference.html#mongoengine.FieldDoesNotExist
    
    
    meta = {
        'strict': False
    }
    

