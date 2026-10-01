from app.models.users import User


class AuthRepository: 
    def __init__(self, session):
        self.session = session

    async def create_user(self, user_data):
        self.session.add(user_data)
        await self.session.commit()
        await self.session.refresh(user_data)
        return user_data

    async def get_user_by_id(self, user_id):
        return await self.session.get(User, user_id)