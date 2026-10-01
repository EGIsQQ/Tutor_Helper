from app.models.student import Students
from sqlalchemy import select

class StudentRepository:
    def __init__(self, session): 
        self.session = session 

    async def create(self, student): 
        self.session.add(student)
        await self.session.commit()
        return student

    async def get_by_id(self, student_id):
        return await self.session.get(Students, student_id)

    async def delete(self, student):
        await self.session.delete(student)
        await self.session.commit()

    async def get_all(self):
        result = await self.session.execute(select(Students).order_by(Students.full_name))
        return result.scalars().all()