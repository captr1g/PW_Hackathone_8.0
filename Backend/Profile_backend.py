from. import Schema
from Database import database
from fastapi import HTTPException, status
from Backend import AuthorizeServer as Auth


def public_profile(username:str, user=database.user):
    profile = user.find_one({"username":username})
    data = {
        "username": profile["username"],
        "name" : profile["name"],
        "email" : profile["email"],
        "gender": profile["gender"],
        "DOB": profile["DOB"],
        "Address": profile["address"]
        }
    return data

def profile_Finder_backend(username: str, user=database.user):
    profile = user.find_one({"username":username})
    friends = user.find_one({"username" : username})['friend']
    if user.username == username:
        return user.username
    elif(username in friends):
        data = {
        "username": profile["username"],
        "name" : profile["name"],
        "email" : profile["email"],
        "phone_number" : profile["phone"],
        "gender": profile["gender"],
        "DOB": profile["DOB"],
        "Address": profile["address"],
        "friends": profile["friends"]
        }
    else:
        user=database.user
        profile = user.find_one({"username":username})
        data = {
            "username": profile["username"],
            "name" : profile["name"],
            "email" : profile["email"],
            "gender": profile["gender"],
            "DOB": profile["DOB"],
            "Address": profile["address"]
        }
        return data