from pymodm import MongoModel, fields
from pymongo.write_concern import WriteConcern

class User(MongoModel):
	phone = fields.CharField(primary_key=True, max_length=11, min_length=11)
	first_name = fields.CharField()
	last_name = fields.CharField()

	class Meta:
		connection_alias = 'my-atlas-app'
		write_concern = WriteConcern(j=True)
		
class History(MongoModel):
	phone = fields.ReferenceField(User)
	time = fields.DateTimeField()
	content = fields.CharField()
	
	class Meta:
		connection_alias = 'my-atlas-app'
		write_concern = WriteConcern(j=True)
	
class Review(MongoModel):
	phone = fields.ReferenceField(User)
	media = fields.CharField()
	rating = fields.IntegerField(max_value=10, min_value=0)
	
	class Meta:
		connection_alias = 'my-atlas-app'
		write_concern = WriteConcern(j=True)