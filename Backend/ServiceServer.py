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
    user.update_one({"username":username}, {'$push':{"transaction":str(data1.inserted_id)}})

def Send_Money(data:Schema.GroupNewTransaction, username:str, user=database.user, transaction=database.transaction):
    amount = data.amount
    receiver = data.receiver.lower()
    password = data.password
    time=datetime.now().strftime("%H:%M:%S")
    today=date.today().strftime("%d-%m-%y")
    profile = user.find_one({"username":username})
    profile1 = user.find_one({"username":receiver})
    
    if not (Auth.verify_password(password, profile['password'])):
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Password!! Transaction Aborted")
    current = profile['balance']
    openbalance = profile1['balance']
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
        user.update_one({"username":username}, {"$push":{"transaction":str(data10.inserted_id)}})
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You don't have enough money")
    
    transaction_info1 = {
        "amount":amount,
        "date":f"{today} {time}",
        "sender":username,
        "recevier":receiver,
        "current_balance":current-amount,
        "status":True
    }
    transaction_info2 = {
        "amount":amount,
        "date":f"{today} {time}",
        "sender":username,
        "recevier":receiver,
        "current_balance":openbalance+amount,
        "status":True
    }
    data1 = transaction.insert_one(transaction_info1)
    data2 = transaction.insert_one(transaction_info2)
    user.update_one({"username":username}, {'$set':{'balance':current-amount}})
    user.update_one({"username":receiver}, {'$set':{'balance':openbalance+amount}})
    user.update_one({"username":username}, {'$push':{"transaction":str(data1.inserted_id)}})
    user.update_one({"username":receiver}, {'$push':{"transaction":str(data2.inserted_id)}})
    return str(data1.inserted_id)

def Get_Remainder(username:str, user=database.user, debt=database.debt):
    all_debt = user.find_one({"username":username})['debt']
    # print(user.find_one({"username":username}))
    print(all_debt[1])
    print((debt.find_one({'_id':all_debt[1]})))
    details = [
        {
            "id":i,
            "amount":debt.find_one({'_id':i})['amount'],
            "lender":debt.find_one({'_id':i})['lender'],
            "date":debt.find_one({'_id':i})['date']
        } for i in all_debt
        if (username in (debt.find_one({'_id':i})['borrower']))
    ]
    print(3)
    return details

def Pay_Debt(data:Schema.PayDebt, username:str, debt=database.debt, user=database.user, transaction=database.transaction):
    detail = debt.find_one({'_id':data.id})
    sender = username
    receiver = detail['lender']
    amount = detail['amount']
    time=datetime.now().strftime("%H:%M:%S")
    today=date.today().strftime("%d-%m-%y")
    password = detail['password']
    profile1 = user.find_one({"username":sender})
    profile2 = user.find_one({"username":receiver})
    if amount < profile1['balance']:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="In-Sufficent Funds")
    if not (Auth.verify_password(password, profile1['password'])):
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Password!! Transaction Aborted")
    transaction_info1 = {
        "amount":amount,
        "date":f"{today} {time}",
        "sender":sender,
        "recevier":receiver,
        "current_balance":profile1['balance']-amount,
        "status":True
    }
    transaction_info2 = {
        "amount":amount,
        "date":f"{today} {time}",
        "sender":sender,
        "recevier":receiver,
        "current_balance":profile2['balance']+amount,
        "status":True
    }
    data1 = transaction.insert_one(transaction_info1)
    data2 = transaction.insert_one(transaction_info2)
    
    user.update_one({"username":username}, {'$set':{'balance':profile1['balance']-amount}})
    user.update_one({"username":receiver}, {'$set':{'balance':profile2['balance']+amount}})
    
    user.update_one({"username":username}, {'$push':{"transaction":str(data1.inserted_id)}})
    user.update_one({"username":receiver}, {'$push':{"transaction":str(data2.inserted_id)}})
    
    debt.update_one({'_id':data.id}, {'$set':{"borrower":detail['borrower'].remove(username)}})
    # user.update_one({"username":username}, {'$set':{"debt":profile1['debt'].remove(data.id)}})
    return str(data1.inserted_id)