#!/usr/bin/python

import pymongo
from pymongo import MongoClient
import string
import random
import os
client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.EcoForecastTest
users = db.users
results = db.results



def mongo_do_authenticate(email, passw):
	u = users.find_one({"email": email})

	if u is None:
		return "user does not exist!"
	elif u["password"] == passw:
		return u["working_dir"]
	else:
		return "user does not exist or password is wrong!"

def mongo_register_user(name, email, affliation, password):

	u = users.find_one({"email": email})
	if u is None:
		try:
			work_dir = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
                	os.system("mkdir users/"+work_dir)
                	os.system("mkdir users/"+work_dir+"/view_results")
			user = {"name": name, "email": email, "affliation": affliation, "password": password, "activate": "Yes", "working_dir": work_dir}
			user_id = users.insert_one(user).inserted_id
			return True
		except:
			return Flase
	else:
		return False


def mongo_get_results(user_id):
	return results.find({"user_id":user_id}).sort("time", -1)


def mongo_get_one_result(user_id, trans_id):
	r = results.find_one({"user_id":user_id, "transaction_id": trans_id})
	return r["result"]








#rec =  results.find()
#for r in rec:
#	print r
#print mongo_do_authenticate("araza@bu.edu")


#print mongo_get_one_result("JWD88O9VHF38", "BDRWVQFUNK")
