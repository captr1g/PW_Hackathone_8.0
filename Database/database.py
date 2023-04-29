from pymongo import MongoClient

client = MongoClient("mongodb+srv://PW_Hackathons:hackathon2.0@payshift.2plumw0.mongodb.net/?retryWrites=true&w=majority", 8000)
db = client["PayShift"]
user = db["Users"]
group = db["Groups"]
transaction = db["Transactions"]
debt=db["Debt"]

# user_data = {
#     "name":"Physics Wallah",
#     "username":"PW_Alokh",
#     "email":"pw_alokh@ineuron.in",
#     "phone":"1234567890",
#     "gender":"O",
#     "dob":"01-01-1971",
#     "password":"None",
#     "address":"Bengaluru",
#     "payment_pref":0,
#     "balance":0.0,
#     "friend":[None],
#     "debt":None,
#     "transaction": [None],
#     "status":False
# }

# debt_data = {
#     "amount":0.0,
#     "lender":None,
#     "borrower":None,
#     "date":"01-01-1971",
#     "cleared":"True"
# }

# transaction_data = {
#     "amount":0.0,
#     "date":"01-01-1971",
#     "sender":None,
#     "receiver":None,
#     "group":None,
#     "current_balance":0.0,
#     "status":False
# }

# group_data = {
#     "group_name":"Hackathon8.0",
#     "group_id":"Hackathon8",
#     "group_member":[None],
#     "group_status":False,
#     "group_transaction":[None]
# }

with open("log.log", mode='a+') as file:
    if (len(client.list_database_names())> 0):
        file.writelines("SUCCESS: MongoDB connection is successful")
    else:
        file.writelines("ERROR: MongoDB connection is failed")
    