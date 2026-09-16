from typing import Annotated

from datetime import datetime

from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.db_depends import get_db
from app.models.lessons_reports import LessonReport
from app.models.student import Students
from app.schemas import CreateLessonReport
from sqlalchemy.orm import selectinload


router = APIRouter(
    prefix="/lesson-reports",
    tags=["Lesson reports"],
)

db = Annotated[AsyncSession, Depends(get_db)]
templates = Jinja2Templates(directory="app/templates")


@router.get("/add", response_class=HTMLResponse)
async def add_lesson_report_page(
    request: Request,
    session: db,
):
    result = await session.execute(
        select(Students).order_by(Students.full_name)
    )
    students = result.scalars().all()

    return templates.TemplateResponse(
        request=request,
        name="add_lesson_report.html",
        context={"students": students},
    )


@router.post("/add")
async def create_lesson_report_from_form(
    session: db,
    student_id: Annotated[int, Form()],
    topic: Annotated[str, Form(min_length=1)],
    lesson_date: Annotated[datetime | None, Form()] = None,
    progress: Annotated[str | None, Form()] = None,
    difficulties: Annotated[str | None, Form()] = None,
    homework: Annotated[str | None, Form()] = None,
    next_lesson_plan: Annotated[str | None, Form()] = None,
    comment: Annotated[str | None, Form()] = None,
):
    student = await session.get(Students, student_id)

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ученик не найден",
        )

    report_data = {
        "student_id": student_id,
        "topic": topic.strip(),
        "progress": progress or None,
        "difficulties": difficulties or None,
        "homework": homework or None,
        "next_lesson_plan": next_lesson_plan or None,
        "comment": comment or None,
    }

    if lesson_date is not None:
        report_data["lesson_date"] = lesson_date

    new_report = LessonReport(**report_data)
    session.add(new_report)
    await session.commit()

    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_lesson_report(
    report: CreateLessonReport,
    session: db,
):
    student = await session.get(Students, report.student_id)

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ученик не найден",
        )

    new_report = LessonReport(
        **report.model_dump(exclude_none=True)
    )

    session.add(new_report)
    await session.commit()
    await session.refresh(new_report)

    return new_report


@router.get("/")
async def get_all_lesson_reports(session: db):
    result = await session.execute(
        select(LessonReport).order_by(
            LessonReport.lesson_date.desc()
        )
    )
    return result.scalars().all()


@router.get("/{student_id}")
async def get_reports_by_student(
    request: Request,
    student_id: int,
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

    return templates.TemplateResponse(
        name="student_reports.html",
        request=request, 
        context={"student":student, "reports": result.scalars().all()},
    )



@router.get("/report_detail/{report_id}", response_class=HTMLResponse)
async def get_report_detail(request: Request, report_id: int, session: db):

    result = await session.execute(
        select(LessonReport)
        .options(selectinload(LessonReport.student))
        .where(LessonReport.id == report_id))
    report = result.scalars().first()
    
    
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Отчёт не найден")
        
   
    return templates.TemplateResponse(
        request=request,
        name="report_detail.html", 
        context={
            "report": report,
        }
    )
