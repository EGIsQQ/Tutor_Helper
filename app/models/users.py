from app.backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship



class User(Base): 
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    role = Column(String(50), nullable=False, default="parent")
    password = Column(String(150), nullable=False)

    student_id = Column(Integer, ForeignKey("student.id"), nullable=True)  

    student = relationship(
            "Students",
            back_populates="user",
        )