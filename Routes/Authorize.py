from fastapi import APIRouter, Depends, status, Request, HTTPException
from fastapi.responses import RedirectResponse

router = APIRouter(tags=['Authentication'])
# db = database.get_db()


