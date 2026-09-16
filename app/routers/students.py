from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.db_depends import get_db
from app.models.lessons_reports import LessonReport
from app.models.student import Students
from app.schemas import CreateStudent

router = APIRouter(
    prefix="/students",
    tags=["Students"],
)

db = Annotated[AsyncSession, Depends(get_db)]
templates = Jinja2Templates(directory="app/templates")


@router.get("/add", response_class=HTMLResponse)
async def add_student_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="add_student.html",
    )


@router.post("/add")
async def create_student_from_form(
    session: db,
    full_name: Annotated[str, Form(min_length=2)],
    subject: Annotated[str | None, Form()] = None,
    level: Annotated[str | None, Form()] = None,
    parent_contact: Annotated[str | None, Form()] = None,
    student_contact: Annotated[str | None, Form()] = None,
):
    new_student = Students(
        full_name=full_name,
        subject=subject or None,
        level=level or None,
        parent_contact=parent_contact or None,
        student_contact=student_contact or None,
    )

    session.add(new_student)
    await session.commit()

    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@router.post('/', status_code=status.HTTP_201_CREATED) 
async def create_student(student: CreateStudent, session: db):
    new_student = Students(**student.model_dump())
    session.add(new_student)
    await session.commit()
    await session.refresh(new_student)
    return new_student

@router.get('/')
async def get_all_students(session: db):
    result = await session.execute(select(Students))
    return result.scalars().all()


@router.get('/{student_id}/reports', response_class=HTMLResponse)
async def student_reports_page(
    student_id: int,
    request: Request,
    session: db,
):
    student = await session.get(Students, student_id)

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ученик не найден",
        )

    result = await session.execute(
        select(LessonReport)
        .where(LessonReport.student_id == student_id)
        .order_by(LessonReport.lesson_date.desc())
    )
    reports = result.scalars().all()

    return templates.TemplateResponse(
        request=request,
        name="student_reports.html",
        context={
            "student": student,
            "reports": reports,
        },
    )


@router.get('/{student_id}')
async def get_student(student_id: int, session: db):
    student = await session.get(Students, student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return student
