from app.backend.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Students(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(150), nullable=False, index=True)
    subject = Column(String(100), nullable=True)
    level = Column(String(100), nullable=True)

    parent_contact = Column(String(150), nullable=True)
    student_contact = Column(String(150), nullable=True)

    lesson_reports = relationship(
    "LessonReport",
    back_populates="student",
    cascade="all, delete-orphan",
    )

    user = relationship(
        "User",
        back_populates="student",
    )