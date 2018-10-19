user_id = "test"
model_name = "test"
interval = "None"
stop_date = "None"
transaction_id = "test"


import os
import subprocess
import json
import pymongo
import random
import time
from pymongo import MongoClient
#os.chdir("/action")
process = subprocess.Popen("/usr/bin/Rscript code.R", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
process.wait()
client = MongoClient('192.1.242.151', 27017)
db = client.EcoForecast
results = db.results
if os.path.isfile("/action/out.json"):
	with open('/action/out.json') as f:
		data = json.load(f)
		result = json.dumps(data)
		print(result)
else:
	result = {"msg": "Error, no result"}
	print(json.dumps(result))

result_data = {
    'user_id': user_id,
    'transaction_id': transaction_id,
    'time': time.asctime(),
    'result': result,
    'model_name': model_name,
    'interval' : interval,
    'stop_date': stop_date
}
results.insert_one(result_data)