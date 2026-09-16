from app.backend.db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text
from datetime import datetime
from sqlalchemy.orm import relationship


class LessonReport(Base):
    __tablename__ = "lesson_reports"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(
        Integer,
        ForeignKey("student.id"),
        nullable=False,
    )

    lesson_date = Column(DateTime, default=datetime.utcnow)
    topic = Column(String(255), nullable=False)       # тема урока
    progress = Column(Text, nullable=True)            # успехи
    difficulties = Column(Text, nullable=True)        # сложности
    homework = Column(Text, nullable=True)            # домашнее задание
    next_lesson_plan = Column(Text, nullable=True)    # план следующего урока
    comment = Column(Text, nullable=True)             # дополнительный комментарий

    student = relationship(
        "Students",
        back_populates="lesson_reports",
    )