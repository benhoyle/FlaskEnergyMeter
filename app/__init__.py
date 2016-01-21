# Import flask and template operators
from flask import Flask, render_template

# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable
from app.energymeter.controllers import energymeter as em

# Import jinja2 filters
#from app.template_filters.filters import filters

app.jinja_env.lstrip_blocks = True
app.jinja_env.trim_blocks = True

# Register blueprint(s)
app.register_blueprint(em)

#app.register_blueprint(filters)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()