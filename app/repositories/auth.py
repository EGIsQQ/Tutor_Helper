from app.models.users import User
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload


class AuthRepository: 
    def __init__(self, session):
        self.session = session

    async def create_user(self, user_data):
        self.session.add(user_data)
        await self.session.commit()
        await self.session.refresh(user_data)
        return user_data

    async def get_user_by_id(self, user_id):
        query = select(User).options(selectinload(User.student)).where(User.id == user_id)
        user = await self.session.scalar(query)
        return user

    async def get_user_by_email(self, email): 
        user = await self.session.scalar(
            select(User).where(User.email == email))
        return user

    async def update_user_students(self, user, student_id):
        query = update(User).where(User.id == user.id).values(student_id=student_id)
        await self.session.execute(query)
        await self.session.commit()

    async def get_user_students(self, user): 
        query = select(User).options(selectinload(User.student)).where(User.id == user.id)
        user_with_students = await self.session.scalar(query)
        return user_with_students.student