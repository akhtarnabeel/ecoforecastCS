import pymongo
from pymongo import MongoClient
client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.EcoForecast
users = db.users
#user = {"name": "Ali Raza", "working_dir":"shit_show", "result": " "}
#user_id = users.insert_one(user).inserted_id
#print user_id


print users.find_one({"name":"Alex"})
