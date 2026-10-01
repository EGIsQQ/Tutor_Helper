from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.backend.db import async_session_maker
from app.models.lessons_reports import LessonReport
from app.models.student import Students
from app.routers import lesson_reports, students, auth
from app.backend.db_depends import get_db


app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

db = Annotated[AsyncSession, Depends(get_db)]


@app.get("/", response_class=HTMLResponse)
async def root(request: Request, session: db):
    students_result = await session.execute(
        select(Students).order_by(Students.full_name)
    )
    all_students = students_result.scalars().all()

    reports_result = await session.execute(
        select(LessonReport)
        .options(selectinload(LessonReport.student))
        .order_by(LessonReport.lesson_date.desc())
        .limit(5)
    )
    
    latest_reports = reports_result.scalars().all()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "students": all_students,
            "reports": latest_reports,
        },
    )


app.include_router(students.router)
app.include_router(lesson_reports.router)
app.include_router(auth.router)