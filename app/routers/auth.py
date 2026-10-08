from fastapi import APIRouter, Depends, status, Request, Form
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies.auth import get_auth_service
from app.models.users import User
from app.schemas.schemas import CreateUser
from typing import Annotated
from app.services.auth import AuthService
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(prefix='/auth', tags=['auth'])
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
    token_new_user = await user_service.create_user(user_data)

    response = RedirectResponse(url=f"/auth/user", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=token_new_user, httponly=True)
    return response

@router.get('/user')
async def get_user_page(request: Request, user_service: Annotated[AuthService, Depends(get_auth_service)]):
    token = request.cookies.get("access_token")
    user = await user_service.get_user_by_token(token)
   
    return templates.TemplateResponse(
        name = "user.html",
        request = request,
        context={"user": user}
    )

@router.get('/login')
async def get_login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )

@router.post('/login')
async def login_user(request: Request, user_service: Annotated[AuthService, Depends(get_auth_service)], form_data: Annotated[OAuth2PasswordRequestForm, Depends()]): 
    token = await user_service.login(form_data.username, form_data.password)

    if token is None:
        return templates.TemplateResponse(
        request=request,
        name="login.html", 
        context={"error": "Неверный email или пароль",
                 "email": form_data.username,
                 "password": form_data.password,} )

    response = RedirectResponse(url="/auth/user", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=token, httponly=True)
    return response
    

