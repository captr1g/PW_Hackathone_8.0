from . import Schema, AuthorizeServer as Auth
from Database import database
from fastapi import HTTPException, status
from datetime import datetime, date

def History(username:str, user=database.user, transaction=database.transaction):
    transaction_id = []
    for i in user.find({'username':username}, {'_id':0, 'transaction':1}):
        transaction_id.append(i)

    data = [
        {
            "date":transaction.find_one({'_id':i})['date'],
            "sender":transaction.find_one({'_id':i})['sender'],
            "receiver":transaction.find_one({'_id':i})['receiver'],
            "group":transaction.find_one({'_id':i})["group"],
            "balance":transaction.find_one({'_id':i})["current_balance"],
            "success":transaction.find_one({'_id':i})["status"],
            "credit":(transaction.find_one({'_id':i})['receiver'] == username)
        } for i in transaction_id
    ]
    return data

def Debt(username:str, user=database.user, debt=database.debt):
    debt_id = []
    for i in user.find({'username':username}, {'_id':0, 'debt':1}):
        debt_id.append(i)
    data = [
        {
            "date":debt.find_one({'_id':i})['date'],
            "lender":debt.find_one({'_id':i})['lender'],
            "amount":debt.find_one({'_id':i})['amount'],
            "balance":debt.find_one({'_id':i})["current_balance"],
            "success":debt.find_one({'_id':i})["status"],
            "status":True if (username in debt.find_one({'_id':i})['borrrower']) else False
        } for i in debt_id
    ]
    return data

def Finance(username:str, user=database.user, debt=database.debt, transaction=database.transaction):
    transaction_id = []
    for i in user.find({'username':username}, {'_id':0, 'transaction':1}):
        transaction_id.append(i)

    data = []
    spend = 0;
    gained = 0;
    shared = 0;
    current = 50000.0
    for i in transaction_id:
        info = {
            "date":transaction.find_one({'_id':i})['date'],
            "sender":transaction.find_one({'_id':i})['sender'],
            "receiver":transaction.find_one({'_id':i})['receiver'],
            "group":transaction.find_one({'_id':i})["group"],
            "balance":transaction.find_one({'_id':i})["current_balance"],
            "success":transaction.find_one({'_id':i})["status"],
            "credit":(transaction.find_one({'_id':i})['receiver'] == username)
        }
        res = transaction.find_one({'_id':i})
        balance = res['current_balance']
        if (current > balance):
            spend += current-balance
        elif (balance > current):
            gained += current-balance
        if res['group'] is not None:
            shared += current-balance
        current = balance
        
        
    return {"transaction":data, "debit":spend, "credit":gained, "splited":shared, "balance":current}