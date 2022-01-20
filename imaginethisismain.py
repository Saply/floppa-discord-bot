from msilib.schema import Class
from mongoengine import *
from data.schemas import *

connect("db-classes")


for clsnames in ClassCollection.objects(class_details__duration = 30):
    print(clsnames.class_details.class_name)

print('\n')


for classes in ClassCollection.objects().filter(id = 3):
    print(f"{classes.id}, {classes.channel_id}, {classes.dates} and class details:\n{classes.class_details.duration}")
print('\n')

# Query using time inside an embedded document
a = ClassCollection.objects().filter(id = 3)

for i in a:
    print(i.class_details.class_name)
# https://stackoverflow.com/questions/36565086/query-embedded-document-list-in-mongoengine
# https://stackoverflow.com/questions/59157791/how-can-you-query-embedded-document-that-is-null-with-mongoengine
# https://docs.mongoengine.org/guide/querying.html
# https://cog-creators.github.io/discord-embed-sandbox/