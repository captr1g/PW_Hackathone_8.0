from fastapi import HTTPException, status, Depends, Request
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2, OAuth2PasswordRequestForm
from fastapi.security.utils import get_authorization_scheme_param
from passlib.context import CryptContext
import Schema
from Database import database
from jose import jwt
from typing import Optional, Dict

class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get("access_token")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization:
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return authorization

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
SECRET_KEY = "25b2e8d86893b06c86bc5a66bfb93ef1ff0de475bb49c7e38280b4d18dd1625a"
oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="login")
ALGORITHM = "HS256"

def hash_pass(password:str):
    return pwd_context.hash(password)

def verify_password(plain_pass:str, hash_pass:str):
    return pwd_context.verify(plain_pass, hash_pass)

def Exist_User(username:str, user=database.db.user):
    return (user.find({"username": username}) > 0)

# def Create_User(data:Schema.Sign_up, database=database.db.user):
#     pass

if Exist_User("1hk"):
    print("Exist")
else:
    print("None")