from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.db_depends import get_db
from app.repositories.student import StudentRepository
from app.services.student import StudentService


async def get_student_repository(session: AsyncSession = Depends(get_db)):
    return StudentRepository(session)

async def get_student_service(repository: StudentRepository = Depends(get_student_repository)):
    return StudentService(repository)