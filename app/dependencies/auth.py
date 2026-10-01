from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.db_depends import get_db
from app.repositories.auth import AuthRepository
from app.services.auth import AuthService


async def get_auth_repository(session: AsyncSession = Depends(get_db)):
    return AuthRepository(session)

async def get_auth_service(repository: AuthRepository = Depends(get_auth_repository)):
    return AuthService(repository)


