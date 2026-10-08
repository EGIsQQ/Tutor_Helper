from typing import Annotated


from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.db_depends import get_db
from app.dependencies.auth import get_auth_service
from app.dependencies.get_user import get_current_user
from app.models.lessons_reports import LessonReport
from app.models.users import User
from app.schemas.schemas import CreateLessonReport, UpdateLessonReport


from app.dependencies.lessons import get_lesson_service
from app.services.lessons import LessonReportService
from app.dependencies.student import get_student_service
from app.services.student import StudentService
from app.services.auth import AuthService


router = APIRouter(
    prefix="/lesson-reports",
    tags=["Lesson reports"],
)

db = Annotated[AsyncSession, Depends(get_db)]
templates = Jinja2Templates(directory="app/templates")


@router.get("/add", response_class=HTMLResponse)
async def add_lesson_report_page(
    request: Request,
    student_service: Annotated[StudentService, Depends(get_student_service)],
):
    students = await student_service.get_all_students()

    return templates.TemplateResponse(
        request=request,
        name="add_lesson_report.html",
        context={"students": students},
    )


@router.post("/add")
async def create_lesson_report_from_form(
    lesson_service: Annotated[LessonReportService, Depends(get_lesson_service)],
    lesson_report: Annotated[CreateLessonReport, Depends(CreateLessonReport.as_form)]
):
    
    report_data = LessonReport(**lesson_report.model_dump())
    await lesson_service.create_report(report_data)

    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)




@router.get("/report_detail/{report_id}", response_class=HTMLResponse)
async def get_report_detail(request: Request, report_id: int,
                             lesson_service: Annotated[LessonReportService, Depends(get_lesson_service)], 
                             user: Annotated[User, Depends(get_current_user)]):
   
    if user.role != "teacher":
        return RedirectResponse(url="/auth/user", status_code=status.HTTP_303_SEE_OTHER)

    report = await lesson_service.get_report_by_id(report_id)
   
    return templates.TemplateResponse(
        request=request,
        name="report_detail.html", 
        context={
            "report": report,
        }
    )


@router.patch("/report_edit/{report_id}")
async def update_lesson_report(
    report_id: int,
    report_data: UpdateLessonReport,
    lesson_service: Annotated[LessonReportService, Depends(get_lesson_service)],
    user: Annotated[User, Depends(get_current_user)]
):
  
    if user.role != "teacher":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to update this report.")
    
    return await lesson_service.update_report(report_id, report_data)

@router.get("/report_edit/{report_id}")
async def edit_lesson_report(
    request: Request,
    report_id: int,
    lesson_service: Annotated[LessonReportService, Depends(get_lesson_service)],
    user: Annotated[User, Depends(get_current_user)]
):

    if user.role != "teacher":
        return RedirectResponse(url="/auth/user", status_code=status.HTTP_303_SEE_OTHER)
    
    report = await lesson_service.get_report_by_id(report_id)

    return templates.TemplateResponse(
        name="edit_report.html",
        request=request,
        context={
            "report": report,
        },
    )

@router.get("/all_reports")
async def get_all_reports(request: Request, lesson_service: Annotated[LessonReportService,
                          Depends(get_lesson_service)], 
                          user_service: Annotated[AuthService, Depends(get_auth_service)]):
    token = request.cookies.get("access_token")
    student = await user_service.get_user_students(token)   
    user = await user_service.get_user_by_token(token)
    reports = await lesson_service.get_lesson_reports_by_student_id(user.student_id)

    return templates.TemplateResponse(
        name="all_reports.html",
        request=request,
        context={
            "reports": reports,
            "student": student,
        },
    )