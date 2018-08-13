import pymongo
from pymongo import MongoClient
client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.EcoForecast
users = db.results
#user = {"name": "Ali Raza", "working_dir":"shit_show", "result": " "}

user = {
    'user_id': "JDMI1TGY3PZI",
    'transaction_id': "transaction_id",
    'time': "time.asctime()",
    'result': "result",
    'model_name': "model_name",
    'interval' : "interval",
    'stop_date': "stop_date"
}

user_id = users.insert_one(user).inserted_id
print user_id

#print db.posts.find()

array =  users.find({"user_id":"JDMI1TGY3PZI"})
for i in array:
	print i 
