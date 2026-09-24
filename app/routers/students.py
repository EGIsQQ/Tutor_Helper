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
    student_data: Annotated[CreateStudent, Depends(CreateStudent.as_form)]
):
    
    new_student = Students(
        **student_data.model_dump()
    )

    session.add(new_student)
    await session.commit()

    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)




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




@router.delete('/{student_id}/reports')
async def delete_student(student_id: int, session: db):
    student = await session.get(Students, student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await session.delete(student)
    await session.commit()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)