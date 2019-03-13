#!/usr/bin/python

import pymongo
from pymongo import MongoClient
import string
import random
import os
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText



client = MongoClient()
client = MongoClient('localhost', 27017, username='openwhisk', password='ecoforecast2019', authSource='EcoForecastTest')
db = client.EcoForecastTest
users = db.users
results = db.results

def mongo_approve_user(who,work_dir):
	if who == "admin":
		users.update_one({"working_dir": work_dir},{"$set": {"admin_appr":"Yes"}})
		return True
	if who == "user":
		users.update_one({"working_dir": work_dir},{"$set": {"email_valid":"Yes"}})
		return True
def mongo_do_authenticate(email, passw):
	u = users.find_one({"email": email})

	if u is None:
		return False, "user does not exist!"
	if u["admin_appr"] != "Yes":
		return False, "user need admin approval!"
	if u["email_valid"] != "Yes":
		return False, "user need to verify email!"
	if u["password"] == passw and u["admin_appr"] == "Yes" and u["email_valid"] == "Yes":
		return True, u["working_dir"]
	else:
		return False, "user does not exist or password is wrong!"

def send_email(who, name, email, affliation, user_id, work_dir):

	fromaddr = "forecasteeco@gmail.com"
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = " "
	msg['Subject'] = "EcoForecast account Authentication!"
	if who == "admin":
		body = ''' Hi, \n You are the admin for EcoForecast. A user just applied for the registration with following information \n Name: {0}  \n email: {1}  \n Affliation: {2} \n Please verify the user by clicking on the link below \n http://ecoforecast.bu.edu/ecoforecastCS/webserver/test/?authen_account=yes&admin={3}'''.format(name, email, affliation, work_dir)
	else:
		body = ''' Hi, \n This a message from EcoForecast. You just applied for the registration with following information \n Name: {0}  \n email: {1}  \n Affliation: {2} \n We are waiting for the admin approval. Please verify your email id  by clicking on the link below \n http://ecoforecast.bu.edu/ecoforecastCS/webserver/test/?authen_account=yes&user={3}'''.format(name, email, affliation, work_dir)

	msg.attach(MIMEText(body, 'plain'))
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, "Check123")
	text = msg.as_string()

	if who =="admin":
		server.sendmail(fromaddr, fromaddr, text)
	else:
		server.sendmail(fromaddr,email, text)
	server.quit()


def mongo_register_user(name, email, affliation, password):

	u = users.find_one({"email": email})
	if u is None:
		try:
			work_dir = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
                	os.system("mkdir users/"+work_dir)
                	os.system("mkdir users/"+work_dir+"/view_results")
			user = {"name": name, "email": email, "affliation": affliation, "password": password, "activate": "Yes", "working_dir": work_dir, "admin_appr": "No", "email_valid":"No"}
			user_id = users.insert_one(user).inserted_id
			send_email("admin", name, email, affliation, user_id, work_dir)
                        send_email("user", name, email, affliation, user_id, work_dir)
			return True
		except:
			return False
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
