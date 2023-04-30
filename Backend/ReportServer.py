from . import Schema, AuthorizeServer as Auth
from Database import database
from fastapi import HTTPException, status
from datetime import datetime, date

def History(username:str, user=database.user, transaction=database.transaction):
    pass