from app import app
from celery import Celery

celery = Celery('app.tasks', broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task
def generate_day(date):
	# Function to generate a new day record for a particular date
	
	# Check whether day already exists
	
		# If day exists exit
	
	# If day doesn't exist:
			
			# Generate pandas dataframe from readings for the date - filter by date
			
			# 
	
    # some long running task here
    return result
