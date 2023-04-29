from pydantic import BaseModel
from typing import List

class Sign_up(BaseModel):
    username: str
    name : str
    email : str
    phone_number : str
    gender: str
    DOB: str
    password : str
    address:str
    
class Log_in(BaseModel):
    username : str
    password : str

class friends_detail(BaseModel):
    name : str
    username : str

class Transaction_detail(BaseModel):
    amount: int 
    date: str
    Money_send: int
    Money_receive: int
    Group_name: str
    Credits: bool
class Profile(BaseModel):
   username: str
   name : str
   email : str
   phone_number : str
   gender: str
   DOB: str
   Address: str
   payment_preference: int
   wallet_balance : int
   friends: List[friends_detail]


class friends_profile(BaseModel):
    username: str
    name : str
    email : str
    phone_number : str
    gender: str
    DOB: str
    Address: str
    friends: List[friends_detail]

class other_profile(BaseModel):
    username: str
    name : str
    email : str
    gender: str
    DOB: str
    Address: str