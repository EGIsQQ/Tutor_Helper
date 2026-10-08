from passlib.context import CryptContext
from app.models.users import User
from app.core.security import create_access_token, get_user_id_from_token
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class AuthService: 
    def __init__(self, repository):
        self.repository = repository

    async def create_user(self, user_data):
        hashed_password = bcrypt_context.hash(user_data.password)
        user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            password=hashed_password,
            role=user_data.role)
        user = await self.repository.create_user(user)
        token = create_access_token(user.id)
        return token

    async def get_user_by_id(self, user_id):
        return await self.repository.get_user_by_id(user_id)

    async def auth_user(self, email, password):
        user = await self.repository.get_user_by_email(email)
        if not user or not bcrypt_context.verify(password, user.password):
            return None
        return user

    async def login(self, email, password): 
        user = await self.auth_user(email, password)

        if user is None:
            return None

        token = create_access_token(user.id)
        return token

    async def get_user_by_token(self, token: str):
        user_id = get_user_id_from_token(token)
        if user_id is None:
            return None
        return await self.get_user_by_id(user_id)

    async def update_user_students(self, token, student_id): 
        user = await self.get_user_by_token(token)
        await self.repository.update_user_students(user, student_id)
       
    async def get_user_students(self, token):
        user = await self.get_user_by_token(token)
        return await self.repository.get_user_students(user)
        
    