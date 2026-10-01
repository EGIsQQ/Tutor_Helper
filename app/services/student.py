from app.models.student import Students 
from fastapi import HTTPException, status

class StudentService:
    def __init__(self, repository):
        self.repository = repository

    async def create_student(self, student_data):
        new_student = Students(**student_data.model_dump())
        return await self.repository.create(new_student)

    async def get_student_by_id(self, student_id):
        student = await self.repository.get_by_id(student_id)
        
        if not student:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Ученик не найден",
                )
        return student

    async def delete_student(self, student_id):
        student = await self.repository.get_by_id(student_id)
        await self.repository.delete(student)

    async def get_all_students(self): 
        return await self.repository.get_all()