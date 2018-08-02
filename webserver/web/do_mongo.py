#!/usr/bin/python

import pymongo
from pymongo import MongoClient
import string
import random
import os
client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.EcoForecast
users = db.users
results = db.results



def mongo_do_authenticate(email):
	u = users.find_one({"email": email})

	if u is None:
		work_dir = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
		os.system("mkdir users/"+work_dir)
		user = {"email": email, "working_dir": work_dir}
		user_id = users.insert_one(user).inserted_id
		return work_dir
	else:
		return u["working_dir"]



def mongo_get_results(user_id):
	return results.find({"user_id":user_id}).sort("time", -1)


#print mongo_do_authenticate("aliraza0337@gmail.com")
