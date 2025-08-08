from pydantic import BaseModel
from enum import Enum

#enum схема для выбора статуса (можно увидеть в /docs)
class TaskStatus(str, Enum):
    new = "новый"
    in_progress = "в процессе выполнения"
    pending = "в ожидании"
    done = "готово"

class TaskCreate(BaseModel):
    title: str
    description: str
    status: str

class TaskRead(TaskCreate):
    id: int

    class Config:
        orm_mode = True