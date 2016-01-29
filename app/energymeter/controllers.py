# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import the database object from the main app module
from app import db

# Import login manager login_required decorator - is there a way to avoid having to add this to all functions in a separate blueprint?
#from flask.ext.login import login_required

# Import module forms
#from app.energymeter.forms import 

# Import module models
from app.energymeter.models import Reading, Day

# Define the blueprint: 'energymeter'
energymeter = Blueprint('energymeter', __name__)

# Import configuration settings
from config import RECORDS_PER_PAGE

@energymeter.route('/', methods=['GET', 'POST'])
@energymeter.route('/index', methods=['GET', 'POST'])
@energymeter.route('/index/<int:page>', methods=['GET', 'POST'])
def index(page=1):
	readings = Reading.query.order_by(Reading.timestamp.desc()).paginate(page, RECORDS_PER_PAGE, False)
	return render_template('dataview.html', readings=readings)
	
@energymeter.route('/day', methods=['GET'])
def showdaydata():
	days = Day.query.order_by(Day.date.desc())
	
	return render_template('dayview.html', days=days)