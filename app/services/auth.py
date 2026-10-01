class AuthService: 
    def __init__(self, repository):
        self.repository = repository

    async def create_user(self, user_data):
        return await self.repository.create_user(user_data)

    async def get_user_by_id(self, user_id):
        return await self.repository.get_user_by_id(user_id)