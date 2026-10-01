from typing import Annotated

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.db_depends import get_db
from app.schemas.schemas import CreateStudent

from app.services.student import StudentService
from app.services.lessons import LessonReportService
from app.dependencies.lessons import get_lesson_service
from app.dependencies.student import get_student_service

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
    student_service: Annotated[StudentService, Depends(get_student_service)],
    student_data: Annotated[CreateStudent, Depends(CreateStudent.as_form)]
):

    await student_service.create_student(student_data)

    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)




@router.get('/{student_id}/reports', response_class=HTMLResponse)
async def student_reports_page(
    student_id: int,
    request: Request,
    lesson_service: Annotated[LessonReportService, Depends(get_lesson_service)],
    student_service: Annotated[StudentService, Depends(get_student_service)]
):
    
    reports = await lesson_service.get_lesson_reports_by_student_id(student_id)
    student = await student_service.get_student_by_id(student_id)

    return templates.TemplateResponse(
        request=request,
        name="student_reports.html",
        context={
            "student": student,
            "reports": reports,
        },
    )




@router.delete('/{student_id}/reports')
async def delete_student(student_id: int, student_service: Annotated[StudentService, Depends(get_student_service)]):
    await student_service.delete_student(student_id)
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)