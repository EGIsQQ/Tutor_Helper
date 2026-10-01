from fastapi import APIRouter, Depends, status, Request
from app.dependencies.auth import get_auth_service
from app.models.users import User
from app.schemas.schemas import CreateUser
from typing import Annotated
from passlib.context import CryptContext
from app.services.auth import AuthService
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(prefix='/auth', tags=['auth'])
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
templates = Jinja2Templates(directory="app/templates")

@router.get('/')
async def get_auth_page(request: Request):
        return templates.TemplateResponse(
        request=request,
        name="register.html")
    

@router.post('/')
async def create_user(user_service: Annotated[AuthService, Depends(get_auth_service)], 
                      create_user: Annotated[CreateUser, Depends(CreateUser.as_form)]):
    
    user_data = User(**create_user.model_dump())
    new_user = await user_service.create_user(user_data)

    return RedirectResponse(url=f"/auth/user/{new_user.id}", status_code=status.HTTP_303_SEE_OTHER)

@router.get('/user/{user_id}')
async def get_user_page(request: Request, user_service: Annotated[AuthService, Depends(get_auth_service)], user_id: int):
    user = await user_service.get_user_by_id(user_id)

    return templates.TemplateResponse(
        name = "user.html",
        request = request,
        context={"user": user}
    )


