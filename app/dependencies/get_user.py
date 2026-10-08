from app.dependencies.auth import get_auth_service
from fastapi import Depends, Request, HTTPException, status
from typing import Annotated
from app.services.auth import AuthService
from app.core.security import get_user_id_from_token


async def get_current_user(request: Request, auth_service: Annotated[AuthService, Depends(get_auth_service)]):
    token = request.cookies.get("access_token")
    if token is None: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    user_id = get_user_id_from_token(token)
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    user = await auth_service.get_user_by_id(user_id)

    return user

