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
   wallet_balance : float
   friends: List[friends_detail]
   

class Token(BaseModel):
    access_token : str
    token_type : str

class UserData(BaseModel):
    username : str

class Group_Transaction(BaseModel):
    transaction_id:str
    per_head_amount:float
    no_of_head:int
    

class GroupInfo(BaseModel):
    group_id : str
    group_name : str
    group_member : List[UserData]
    group_transaction : List[Group_Transaction]

class AllGroup(BaseModel):
    group_id:str
    group_name:str
    group_member:int

class AddGroup(BaseModel):
    group_name:str
    group_member:List[str]


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

class GroupNewTransaction(BaseModel):
    receiver:str
    amount:float
    password:str

class AddMoney(BaseModel):
    amount:float
    
    