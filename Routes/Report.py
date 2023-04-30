from typing import List
from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import RedirectResponse
from Backend import Schema, ReportServer, AuthorizeServer as Auth

