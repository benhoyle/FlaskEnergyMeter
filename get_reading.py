# Import pyserial library to access meter
import serial
# Import re to decode xml
import re
# Import time functions for delay
import time
# Import database and models
from app import db
from app.energymeter.models import Reading

def main():
	
	port 		=	'/dev/ttyUSB0'
	baud 		=	57600
	timeout 	=	10
	
	while True:
		try:
			meter		=	serial.Serial(port, baud, timeout=timeout)
			data		=	meter.readline()
			meter.close()
		except SerialException:
			print "Could not access device. Trying again in 30s. \n"
			# Try again  in 30s
			time.sleep(30)
			
		else:
			#print data # For testing
			
			watts_ex	= 	re.compile('<watts>([0-9]+)</watts>')
			temp_ex		= 	re.compile('<tmpr>([0-9\.]+)</tmpr>')
			
			raw_watts	=	watts_ex.findall(data)
			if raw_watts:
				watts 	= 	int(raw_watts.pop())
				#print watts # For testing
				
			raw_temp	=	temp_ex.findall(data)
			if raw_temp:
				temp	=	float(raw_temp.pop())
				#print temp # For testing
			
			if watts and temp:
				reading 	=	Reading(watts, temp)
				#print "Adding Reading" # For testing
				db.session.add(reading)
				db.session.commit()
			
			# Sleep for 2 minutes
			time.sleep(120)
	
if __name__ == "__main__":
	main()
