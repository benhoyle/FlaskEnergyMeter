FlaskEnergyMeter 
================
A revised version of the Energy Meter visualisation that uses Flask.

User running get_reading.py needs to be a member of group 'dialout':

```bash
sudo adduser <youruser> dialout
```
Then logout and login or restart. You can check user is member of 
dialout group by running:
```bash
id <youruser>
```

Run the get_reading.py file in the background using:
```bash
nohup python get_reading.py > /dev/null 2>readings.log &
```
(This logs any screen output to a readings.log file.)
