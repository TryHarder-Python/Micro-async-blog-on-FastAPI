import datetime
from typing import Optional
from pydantic import UUID4, BaseModel, EmailStr, Field, validator


class UserCreate(BaseModel):
    """Проверяет sing-up запрос"""
    email: EmailStr
    name: str
    password: str


class UserBase(BaseModel):
    """Формирует тело ответа с деталями пользывателя"""
    id: int
    email: EmailStr
    name: str


class TokenBase(BaseModel):
    """Формирует токен"""
    token: UUID4 = Field(..., alias='access_token')
    expire: datetime
    token_type: Optional[str] = 'bearer'

    class Config:
        allow_population_by_field_name = True

    @validator('token')
    def hexlify_token(cls, value):
        """Конвертирует UUID в hex строку"""
        return value.hex


class User(BaseModel):
    """Формирует тело ответа с детялами пользывателя и токеном"""
    token: TokenBase = {}