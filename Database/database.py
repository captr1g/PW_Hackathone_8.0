from pymongo import MongoClient

client = MongoClient("mongodb+srv://PW_Hackathons:hackathon2.0@payshift.2plumw0.mongodb.net/?retryWrites=true&w=majority", 8000)
db = client["PayShift"]

with open("log.log", mode='a+') as file:
    if (len(client.list_database_names())> 0):
        file.writelines("SUCCESS: MongoDB connection is successful")
    else:
        file.writelines("ERROR: MongoDB connection is failed")
    