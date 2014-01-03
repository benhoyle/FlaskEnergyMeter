from flask import Flask, request, render_template, g 

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pygal
from pygal.style import CleanStyle
import ConfigParser

app = Flask(__name__)

#Get settings
parser = ConfigParser.SafeConfigParser()
parser.read('config.ini')
DATABASE = parser.get('Path Config', 'DATABASE')
host_ip = parser.get('Host Config', 'ip')
host_port = parser.getint('Host Config', 'port')
debug_config = parser.getboolean('Host Config', 'debug')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv
    
def crop_time(datetime_str):
	T_index = datetime_str.find("T")
	return datetime_str[0:(T_index+6)]

@app.route("/", methods=['GET', 'POST'])
def plot_chart():
	if request.method == 'GET':
		return render_template("index.html", title=None)
	
	if request.method == 'POST':
		variable = request.form['variable']
		units = request.form['units']
		#Crop time to accomodate browser differences
		startdatetime = crop_time(request.form['startdatetime'])
		enddatetime = crop_time(request.form['enddatetime'])
		#Need to look at how safari renders datetimes
		#Chrome datetime-local - 2013-12-20T00:00
		# atomic ipad - 2013-12-17T19:45:462013-12-18T19:45:50.094
		
		sdt = datetime.strptime(startdatetime,"%Y-%m-%dT%H:%M")
		edt = datetime.strptime(enddatetime, "%Y-%m-%dT%H:%M")
		
		
		qry = "SELECT * FROM readings WHERE r_datetime > '%(sdt)s' AND r_datetime < '%(edt)s'" % {'sdt': startdatetime, 'edt':enddatetime}
		#each row is of the form (u'2013-12-16 00:15:02.911489', 278, 18.4) 
		rows = query_db(qry)
		
		df = pd.DataFrame(rows)
		df.columns = ["dt","watts","temp"]
		df.index = pd.to_datetime(df.pop("dt"))
		graph_data = df
		
		#Find means for time periods by resampling
		if units == "Hours":
			graph_data = df.resample('1H', how='mean')
		if units == "Days":
			graph_data = df.resample('1D', how='mean')
		if units == "Weeks":
			graph_data = df.resample('1W', how='mean')
		if units == "Months":
			graph_data = df.resample('1M', how='mean')
		if units == "Years":
			graph_data = df.resample('1Y', how='mean')
		
		if variable == "Watts":
			data = [(graph_data.index[i], graph_data.watts[i]) for i in range(0, len(graph_data))]
		if variable == "Temperature":
			data = [(graph_data.index[i], graph_data.temp[i]) for i in range(0, len(graph_data))]
			#the above could be performed by selecting a different query
		
		#Draw chart
		datey = pygal.DateY(x_label_rotation=20, style=CleanStyle, show_dots=False)
		#xlabels have a bug - appears to be there on website example
		datey.add(variable, data)
		return datey.render() 
		

if __name__ == "__main__":
	app.run(host=host_ip, port=host_port, debug=debug_config)
