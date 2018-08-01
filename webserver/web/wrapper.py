


import os
import subprocess
import json
import pymongo
import random
from pymongo import MongoClient
os.chdir("/action")

process = subprocess.Popen("/usr/bin/Rscript code.R", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
process.wait()
client = MongoClient('192.1.242.152', 27017)
db = client.EcoForecast
posts = db.posts
if os.path.isfile("out.json"):
	with open('out.json') as f:
		data = json.load(f)
		result = json.dumps(data)
		print(result)
else:
	result = {"msg": "Error, no result"}
	print(json.dumps(result))

post_data = {
    'user id': user_id,
    'action name': action_name,
    'action id': str(random.randint(1,213432)),
    'result' : result
}
posts.insert_one(post_data)