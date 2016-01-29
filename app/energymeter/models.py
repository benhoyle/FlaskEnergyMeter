# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db

# Import datetime for time functions
from datetime import datetime

# Import pandas
import pandas as pd

import pickle

# Import costs from config file
from config import KWH_COST, STANDING_CHARGE



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

# You should be able to use an abstract class for some of the attributes and methods of the classes below

class Day(db.Model):

	__tablename__  	=	'day'
	
	id            	= 	db.Column(db.Integer, primary_key=True)
	# Number of day in year - e.g. 1 to 365 / 366
	number			=	db.Column(db.Integer)
	date			=	db.Column(db.Date)
	year			=	db.Column(db.Integer)
	dataframe		=	db.Column(db.PickleType)
	# Number of kwhs used in the day
	units_used		=	db.Column(db.Numeric)
	# Cost of units used
	cost_units		=	db.Column(db.Numeric)
	# Total cost including standing charge
	cost_total		=	db.Column(db.Numeric)
	
	def __init__(self, date):
		self.date 	= 	date
		self.number	=	date.timetuple().tm_yday
		self.year	=	date.timetuple().tm_year
	
	@classmethod
	def get(cls, date, create=False):
		# Method to get a day record for a supplied date - if create=true the method will create and return a new day object if no pre-existing object exists
		existing_day	=	cls.query.filter(cls.date == date.date()).first()
		if not existing_day and create:
			existing_day 	=	cls(date)
			db.session.add(existing_day)
			db.session.commit()
		if existing_day:
			return existing_day
		else:
			return None
			
	@classmethod
	def generate_all(cls, overwrite=False):
		# Generate day records for all days where we have recorded timestamps
		# Get list of distinct dates in Reading
		distinct_dates = db.session.query(db.func.DATE(Reading.timestamp)).distinct().all()
		# Convert to datetime objectd
		distinct_dates = [datetime.strptime(date[0], '%Y-%m-%d') for date in distinct_dates]
		for date in distinct_dates:
			if not cls.get(date) or overwrite:
				new_day = cls.get(date, create=True)
				new_day.get_cost(overwrite=True)
	
	def get_dataframe(self, overwrite=False):
		# Method to generate and store dataframe
		#if overwrite=True a new dataframe will be generated and the old frame will be overwritten
		#if overwrite=False no new dataframe will be generated if one already exists
		if self.dataframe and not overwrite:
			return pickle.loads(self.dataframe)
		else:
			columns 		= 	[c.name for c in Reading.__table__.columns]
			columns.remove("id")
			def make_row(x):
				return dict([(c, getattr(x, c)) for c in columns])
			query 			= 	Reading.query.filter(db.func.date(Reading.timestamp) == self.date)
			dataframe	=	pd.DataFrame([make_row(x) for x in query])
			
			dataframe.index = pd.to_datetime(dataframe.pop("timestamp"))
			#Resample to standard 2minute intervals
			dataframe = dataframe.resample("2T", how="mean")
			# Resample here to common timebase? e.g. every 2mins + fill missmg data
			start = datetime(self.date.year, self.date.month, self.date.day, 0, 0)
			end = datetime(self.date.year, self.date.month, self.date.day, 23, 59)
			dayrange = pd.date_range(start, end, freq="2min")
			dataframe = dataframe.reindex(dayrange)
			dataframe.sort_index
			self.dataframe = pickle.dumps(dataframe)
			db.session.add(self)
			db.session.commit()
			return dataframe
	
	def get_cost(self, overwrite=False):
		if not (self.units_used and self.cost_units and self.cost_total) or overwrite:
			df = self.get_dataframe(overwrite=True)
			df_hour = df["watt"].resample("1H", how="sum")
			df_kwh = df_hour/(30*1000)
			self.units_used = df_kwh.sum()
			self.cost_units = (KWH_COST*self.units_used)/100
			self.cost_total = self.cost_units + STANDING_CHARGE/100
			db.session.add(self)
			db.session.commit()
		return {
					'units_used'	:	format(self.units_used, ',.2F'), 
					'cost_units'	:	format(self.cost_units, ',.2F'),
					'cost_total'	:	format(self.cost_total, ',.2F')
					}
	
	def get_plot(self, yaxis="W"):
		# Returns a plot of hourly energy usage for "W" or temperature for "T"
		pass
		



class Week(db.Model):

	__tablename__  	=	'week'
	
	id            	= 	db.Column(db.Integer, primary_key=True)
	# Number of week in year - from 1 to 52
	number			=	db.Column(db.Integer)
	year			=	db.Column(db.Integer)
	dataframe		=	db.Column(db.PickleType)
	# Number of kwhs used in the week
	units_used		=	db.Column(db.Numeric)
	# Cost of units used in the week
	cost_units		=	db.Column(db.Numeric)
	# Total cost including standing charge for the week
	cost_total		=	db.Column(db.Numeric)
	# Average daily usage for the week
	av_day_units	=	db.Column(db.Numeric)
	# Average daily cost for the week
	av_day_tcost	=	db.Column(db.Numeric)
	
	# Use function to return start date / end date
	
	def get_plot(self, yaxis="W"):
		# Returns a plot of daily energy usage for the week "W" or average hourly temperature over the week for "T"
		pass

class Month(db.Model):

	__tablename__  	=	'month'

	id            	= 	db.Column(db.Integer, primary_key=True)
	# Number of month in year - from 1 to 12
	number			=	db.Column(db.Integer)
	year			=	db.Column(db.Integer)
	dataframe		=	db.Column(db.PickleType)

class Year(db.Model):

	__tablename__  	=	'year'
	
	id            	= 	db.Column(db.Integer, primary_key=True)
	year			=	db.Column(db.Integer)
	
	# Use function to return the 12 month dataframes