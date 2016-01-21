# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db

# Import datetime for time functions
from datetime import datetime

# Define a Case model
class Reading(db.Model):

	__tablename__  	=	'reading'
	
	id            	= 	db.Column(db.Integer, primary_key=True)
	timestamp		=	db.Column(db.DateTime)
	watt			=	db.Column(db.Integer)
	temperature		=	db.Column(db.Float)
	
	def __init__(self, watt, temp):
		self.timestamp		=	datetime.now()
		self.watt			=	watt
		self.temperature	=	temp
	