from . import Schema
from Database import database
from fastapi import HTTPException, status

def Get_Group(username:str, group_id:str, groups=database.group):
    if username in groups.find_one({"group_id":group_id, "group_status":True}, {"_id":0, "group_member":1})["group_member"]:
        information = groups.find_one({"group_id":group_id})
        result_data =Schema.GroupInfo(
            group_id=group_id,
            group_name=information['group_name'],
            group_member=[Schema.UserData(username=i) for i in information['group_member']],
            group_transaction=[
                Schema.Group_Transaction(
                    transaction_id=i['transaction_id'],
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
    group_data = {
        "group_name":data.group_name,
        "group_id":"Hackathon8",
        "group_member":data.group_member,
        "group_status":True,
        "group_transaction":[None]
    }
    
        