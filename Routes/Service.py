from typing import List
from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from Backend import Schema, ServiceServer, AuthorizeServer as Auth

router = APIRouter(prefix='/services', tags=['Services'])
template = Jinja2Templates(directory="Frontend")


@router.get("/", response_class=HTMLResponse ,status_code=status.HTTP_302_FOUND)
def service_home(request:Request, current_user:Schema.UserData=Depends(Auth.get_current_user)):
    return template.TemplateResponse("services.html", {"request":request})

@router.post("/add", status_code=status.HTTP_202_ACCEPTED)
def add_money(request:Schema.AddMoney, current_user:Schema.UserData=Depends(Auth.get_current_user)):
    money = ServiceServer.Add_Money(request, current_user.username)
    return money

@router.get("/add", status_code=status.HTTP_202_ACCEPTED)
def add_money(request:Schema.AddMoney, current_user:Schema.UserData=Depends(Auth.get_current_user)):
    return template.TemplateResponse("addm.html", {"request":request})

@router.post("/send", status_code=status.HTTP_202_ACCEPTED)
def send_money(request:Schema.GroupNewTransaction, current_user:Schema.UserData=Depends(Auth.get_current_user)):
    money = ServiceServer.Send_Money(request, current_user.username)
    return money

@router.get("/remainder", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
def get_remainder(request:Request, current_user:Schema.UserData=Depends(Auth.get_current_user)):
    remainder = ServiceServer.Get_Remainder(current_user.username)
    # print(remainder)
    # return remainder
    return template.TemplateResponse("debt.html",{"request":request, "remaninder": remainder})


@router.post("/remainder", status_code=status.HTTP_202_ACCEPTED, response_class=HTMLResponse)
def pay_debt(request:Schema.PayDebt, current_user:Schema.UserData=Depends(Auth.get_current_user)):
    payment = ServiceServer.Pay_Debt(request, current_user.username)
    return payment
    
    