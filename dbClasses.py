from pymodm import MongoModel, fields
from pymongo.write_concern import WriteConcern

class User(MongoModel):
    phone = fields.CharField(primary_key=True, max_length=11, min_length=11)
    firstName = fields.CharField(blank=True)
    lastName = fields.CharField(blank=True)

    class Meta:
        connection_alias = 'my-atlas-app'
        write_concern = WriteConcern(j=True)

class History(MongoModel):
    phone = fields.ReferenceField(User)
    time = fields.DateTimeField(required=True)
    content = fields.CharField(required=True)

    class Meta:
        connection_alias = 'my-atlas-app'
        write_concern = WriteConcern(j=True)

class Review(MongoModel):
    phone = fields.ReferenceField(User)
    title = fields.CharField(required=True)
    season = fields.IntegerField(blank=True)
    episode = fields.IntegerField(blank=True)
    rating = fields.FloatField(required=True, max_value=10, min_value=0)

    class Meta:
        connection_alias = 'my-atlas-app'
        write_concern = WriteConcern(j=True)
        