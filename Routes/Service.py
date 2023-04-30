from typing import List
from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import RedirectResponse
from Backend import Schema, ServiceServer, AuthorizeServer as Auth

router = APIRouter(prefix='/services', tags=['Services'])

@router.get("/", status_code=status.HTTP_302_FOUND)
def service_home(request:Request, current_user:Schema.UserData=Depends(Auth.get_current_user)):
    pass

@router.post("/add", status_code=status.HTTP_202_ACCEPTED)
def add_money(request:Schema.AddMoney, current_user:Schema.UserData=Depends(Auth.get_current_user)):
    money = ServiceServer.Add_Money(request, current_user.username)
    return money

@router.post("/send", status_code=status.HTTP_202_ACCEPTED)
def send_money(request:Schema.GroupNewTransaction, current_user:Schema.UserData=Depends(Auth.get_current_user)):
    money = ServiceServer.Send_Money(request, current_user.username)
    return money

@router.get("/remainder", status_code=status.HTTP_200_OK)
def get_remainder(request:Request, current_user:Schema.UserData=Depends(Auth.get_current_user)):
    # print(1)
    remainder = ServiceServer.Get_Remainder(current_user.username)
    return remainder

@router.post("/remainder", status_code=status.HTTP_202_ACCEPTED)
def pay_debt(request:Schema.PayDebt, current_user:Schema.UserData=Depends(Auth.get_current_user)):
    payment = ServiceServer.Pay_Debt(request, current_user.username)
    return payment
    
    