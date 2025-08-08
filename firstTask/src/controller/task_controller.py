from fastapi import HTTPException
from src.usecase.task_usecase import TaskUseCase
from src.models.schemas import TaskCreate

#Проверяем наличие таска по id и в случае если ничего нет то уведомляем об отсутствии тасков
class TaskController:
    @staticmethod
    def get_task(task_id: int):
        task = TaskUseCase.get_task(task_id)
        if task is None:
            raise HTTPException(
                status_code=404,
                detail="Задача не найдена"
            )
        return task

    @staticmethod
    def create_task(task_data: TaskCreate):
        return TaskUseCase.create_task(task_data)
    