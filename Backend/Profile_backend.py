from. import Schema
from Database import database
from fastapi import HTTPException, status


def profile_Finder(request: request, username: str):
    