from datetime import datetime

from pydantic import BaseModel


class PostModel(BaseModel):
    """ Валидатор для требуемого поста """
    title: str
    content: str


class PostDetailsModel(PostModel):
    """ Для ответа о одном посте """
    id: int
    create_at: datetime
    user_name: str