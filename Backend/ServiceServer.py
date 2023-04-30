from . import Schema, AuthorizeServer as Auth
from Database import database
from fastapi import HTTPException, status
from datetime import datetime, date

def Add_Money(data:Schema.AddMoney, username:str, user=database.user, transaction=database.transaction):
    amount = data.amount
    password = data.password
    time=datetime.now().strftime("%H:%M:%S")
    today=date.today().strftime("%d-%m-%y")
    profile = user.find_one({"username":username})
    if not (Auth.verify_password(password, profile['password'])):
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Password!! Transaction Aborted")
    current = profile['balance']+amount
    user.update_one({"username":username}, {'$set':{'balance':current}})
    transaction_info = {
        "amount":amount,
        "date":f"{today} {time}",
        "sender":username,
        "receiver":username,
        "current_balance":current,
        "status":True
    }
    data1 = transaction.insert_one(transaction_info)
    user.update_one({"username":username}, {'$push':{"transaction":data1.inserted_id}})

def Send_Money(data:Schema.GroupNewTransaction, username:str, user=database.user, transaction=database.transaction):
    amount = data.amount
    receiver = data.receiver.lower()
    password = data.password
    time=datetime.now().strftime("%H:%M:%S")
    today=date.today().strftime("%d-%m-%y")
    profile = user.find_one({"username":username})
    
    if not (Auth.verify_password(password, profile['password'])):
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Password!! Transaction Aborted")
    current = profile['balance']
    if current < amount:
        transaction_info = {
            "amount":amount,
            "date":f"{today} {time}",
            "sender":username,
            "receiver":receiver,
            "current_balance":profile['balance'],
            "status":False
        }
        data10 = transaction.insert_one(transaction_info)
        user.update_one({"username":username}, {"$push":{"transaction":data10.inserted_id}})
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You don't have enough money")
    
    transaction_info = {
        "amount":amount,
        "date":f"{today} {time}",
        "sender":username,
        "recevier":receiver,
        "current_balance":current-amount,
        "status":True
    }
    data1 = transaction.insert_one(transaction_info)
    user.update_one({"username":username}, {'$set':{'balance':current-amount}})
    user.update_one({"username":receiver}, {'$set':{'balance':current+amount}})
    user.update_one({"username":username}, {'$push':{"transaction":data1.inserted_id}})
    user.update_one({"username":receiver}, {'$push':{"transaction":data1.inserted_id}})

