from . import Schema
from Database import database
from fastapi import HTTPException, status

def Get_Group(username:str, group_id:str, groups:database.group):
    if username in groups.find_one({"group_id":group_id}, {"_id":0, "group_member":1})["group_member"]:
        information = {
            
        }

