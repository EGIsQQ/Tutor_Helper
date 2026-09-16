from pydantic import BaseModel
from datetime import datetime

class CreateStudent(BaseModel):
    full_name: str
    subject: str | None = None
    level: str | None = None
    parent_contact: str | None = None
    student_contact: str | None = None

class CreateLessonReport(BaseModel):
    student_id: int
    topic: str
    lesson_date: datetime | None = None
    progress: str | None = None
    difficulties: str | None = None
    homework: str | None = None
    next_lesson_plan: str | None = None
    comment: str | None = None