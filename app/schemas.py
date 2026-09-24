from pydantic import BaseModel
from datetime import datetime
from fastapi import Form

class CreateStudent(BaseModel):
    full_name: str
    subject: str | None = None
    level: str | None = None
    parent_contact: str | None = None
    student_contact: str | None = None

    @classmethod
    def as_form(
        cls,
        full_name: str = Form(),
        subject: str | None = Form(default=None),
        level: str | None = Form(default=None),
        parent_contact: str | None = Form(default=None),
        student_contact: str | None = Form(default=None), 
        ):

        return cls(
            full_name=full_name,
            subject=subject,
            level=level,
            parent_contact=parent_contact,
            student_contact=student_contact,
        )

class CreateLessonReport(BaseModel):
    student_id: int
    topic: str
    lesson_date: datetime | None = None
    progress: str | None = None
    difficulties: str | None = None
    homework: str | None = None
    next_lesson_plan: str | None = None
    comment: str | None = None

class UpdateLessonReport(BaseModel):
    topic: str | None = None
    lesson_date: datetime | None = None
    progress: str | None = None
    difficulties: str | None = None
    homework: str | None = None
    next_lesson_plan: str | None = None
    comment: str | None = None