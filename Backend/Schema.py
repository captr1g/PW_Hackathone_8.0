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
    
class Log_in(BaseModel):
    username : str
    password : str

class friends_detail(BaseModel):
    name : str
    username : str


class Profile(BaseModel):
   username: str
   name : str
   email : str
   phone_number : str
   gender: str
   DOB: str
   payment_preference: int
   wallet_balance : int
   friends: List[friends_detail]
