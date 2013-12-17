from flask import Flask
import yaml
app = Flask(__name__)
app.config.from_object('config')
app.cfg = {'temp_set': 10, 'temp_delta': 0.25, 'valve_work': 40, 'valve_delta': 3}

f=open('/home/pi/reletherm.cfg', 'r')
app.cfg = yaml.safe_load(f)
f.close()
		

from app import views
