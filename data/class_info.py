import mongoengine 

class ClassInfo(mongoengine.EmbeddedDocumentField):
    _id = mongoengine.SequenceField()
    