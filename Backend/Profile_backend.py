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
        "DOB": profile["dob"],
        "Address": profile["address"]
        }
    return data

def profile_Finder_backend(username: str, current_user:str, user=database.user):
    profile = user.find_one({"username":username})
    print(profile)
    friends = profile['friend']
    print(friends,  username, "sothing oiguj")
    if user["username"] == username:
        return user.username
    elif(current_user in friends):
        print("inside the if")
        data = {
        "username": profile["username"],
        "name" : profile["name"],
        "email" : profile["email"],
        "phone_number" : profile["phone"],
        "gender": profile["gender"],
        "DOB": profile["dob"],
        "Address": profile["address"],
        "friends": profile["friend"]
        }
        return data
    else:
        user=database.user
        profile = user.find_one({"username":username})
        data = {
            "username": profile["username"],
            "name" : profile["name"],
            "email" : profile["email"],
            "gender": profile["gender"],
            "DOB": profile["dob"],
            "Address": profile["address"]
        }
        return data