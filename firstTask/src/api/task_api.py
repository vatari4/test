from fastapi import APIRouter
from src.controller.task_controller import TaskController
from src.models.schemas import TaskCreate, TaskRead

router = APIRouter()

#Вызываем из контролера получение тасков по id
@router.get("/task/{task_id}", response_model=TaskRead)
async def get_task(task_id: int):
    return TaskController.get_task(task_id)

#Вызываем из контролера для создания тасков
@router.post("/task", response_model=TaskRead)
async def create_task(task_data: TaskCreate):
    return TaskController.create_task(task_data)
