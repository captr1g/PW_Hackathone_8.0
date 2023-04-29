# from enum import member
from . import Schema
from Database import database
from fastapi import HTTPException, status
from datetime import datetime, date

def Get_Group(username:str, group_id:str, groups=database.group):
    if username in groups.find_one({"group_id":group_id, "group_status":True}, {"_id":0, "group_member":1})["group_member"]:
        information = groups.find_one({"group_id":group_id})
        result_data =Schema.GroupInfo(
            group_id=group_id,
            group_name=information['group_name'],
            group_member=[Schema.UserData(username=i) for i in information['group_member']],
            group_transaction=[
                Schema.Group_Transaction(
                    transaction_id=i['_id'],
                    per_head_amount=i['per_head_amount'],
                    no_of_head=i['no_of_head']
                ) for i in information['group_transaction']
            ]
        )
        return result_data
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No Such Group Exist")

def Gell_All_Group(username:str, groups=database.group):
    all_group=[]
    for i in groups.find({}, {'group_id':1, 'group_member':1}):
        if username in i['group_member']:
            all_group.append(i['group_id'])
    if len(all_group) == 0:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="User doesn't have any group")
    else:
        result_data = [
            Schema.AllGroup(
                group_id=i,
                group_name=groups.find_one({"group_id":i})['group_name'],
                group_member=len(groups.find_one({"group_id":i})['group_member'])
            ) for i in all_group
        ]
        return result_data

def Add_Group(data:Schema.AddGroup, username:str, groups:database.group):
    time=datetime.now().strftime("%H%M%S")
    today=date.today().strftime("%d%m%y")
    data.group_member.append(username)
    group_data = {
        "group_name":data.group_name,
        "group_id":f"{data.group_name.split(' ')[0]}{today}{time}",
        "group_member":data.group_member,
        "group_status":True,
        "group_transaction":[None]
    }
    id = groups.insert_one(group_data)
    return id.inserted_id


def Find_Friend(username:str, user:database.user):
    result_data = [
        Schema.UserData(username=i)
        for i in user.find_one({"username":username})['friend']
    ]
    return result_data

def New_Transaction(amount:float, group_id:str, username:str, user=database.user, group=database.group, transaction=database.transaction, debt=database.debt):
    time=datetime.now().strftime("%H:%M:%S")
    today=date.today().strftime("%d-%m-%y")
    profile = user.find_one({"username":username})
    current = profile['balance']
    if current < amount:
        transaction_info = {
            "amount":amount,
            "date":f"{today} {time}",
            "sender":username,
            "group":group_id,
            "current_balance":profile['balance'],
            "status":False
        }
        transaction.insert_one(transaction_info)
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You don't have enough money")
    new_balance = current-amount
    user.update_one({"username":username}, {'$set':{'balance':new_balance}})
    
    transaction_info = {
        "amount":amount,
        "date":f"{today} {time}",
        "sender":username,
        "group":group_id,
        "current_balance":new_balance,
        "status":True
    }
    data1 = transaction.insert_one(transaction_info)

    grouped = group.find_one({"group_id":group_id})
    members = grouped['members']
    grouped_info = {
        "transaction_id":data1.inserted_id,
        "per_head_amount":amount/len(members),
        "no_of_head":len(members)
    }
    data2 = grouped['group_transaction'].insert_one(grouped_info)

    borrower = [i for i in members if i != username]
    debt_info = {
        "amount":amount/len(members),
        "lender":username,
        "borrower":borrower,
        "date":f"{today} {time}",
        "cleared":False
    }
    data3 = debt.insert_one(debt_info)

    for i in members:
        if i != username:
            user.update_one({"username":i}, {'$set':{'debt':data3.inserted_id}})
    # group_info
    return data1.inserted_id