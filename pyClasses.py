import datetime

class pyUser(object):
	
	def __init__(self, phone, firstName=None, lastName=None):
		self.phone = phone
		self.firstName = firstName
		self.lastName = lastName
		
class pyHistory(object):
	
	def __init__(self, phone, content, time=datetime.datetime.now()):
		self.phone = phone
		self.content = content
		self.time = time
		
class pyReview(object):
	
	def __init__(self, phone, title=None, rating=None):
		self.phone = phone
		self.title = title
		self.rating = rating