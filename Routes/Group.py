from typing import List
from fastapi import APIRouter, Depends, status, Request, HTTPException
from fastapi.responses import RedirectResponse
from Backend import Schema, GroupServer, AuthorizeServer as Auth

router = APIRouter(prefix='/groups', tags=['Groups'])

@router.get("/", status_code=status.HTTP_302_FOUND)
def redirect_to_groups(request:Request, current_user:Schema.UserData=Depends(Auth.get_current_user)):
    return RedirectResponse('all')

@router.get("/all", response_model=List[Schema.AllGroup], status_code=status.HTTP_202_ACCEPTED)
def all_groups(request:Request, current_user:Schema.UserData=Depends(Auth.get_current_user)):
    groups = GroupServer.Get_All_Group(current_user)
    return groups

@router.get("/{group_id}", response_model=Schema,status_code=status.HTTP_200_OK)
def group_detail(request:Request, group_id:str, current_user:Schema.UserData=Depends(Auth.get_current_user)):
    group = GroupServer.Get_Group(current_user, group_id)
    return group

@router.post("/create", status_code=status.HTTP_201_CREATED)
def new_group(request:Schema.AddGroup, current_user:Schema.UserData=Depends(Auth.get_current_user)):
    new_group = GroupServer.Add_Group(request, current_user)
    return new_group