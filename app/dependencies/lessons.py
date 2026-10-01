from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.db_depends import get_db
from app.repositories.lessons import LessonReportRepository
from app.services.lessons import LessonReportService


async def get_lesson_repository(session: AsyncSession = Depends(get_db)):
    return LessonReportRepository(session)

async def get_lesson_service(repository: LessonReportRepository = Depends(get_lesson_repository)):
    return LessonReportService(repository)