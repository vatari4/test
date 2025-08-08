from src.models.db import get_db
from src.models.task import Task
from src.models.schemas import TaskCreate

class TaskUseCase:
    @staticmethod
    def get_task(task_id: int):
        db = next(get_db())
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return None
        return task

    @staticmethod
    def create_task(task_data: TaskCreate):
        db = next(get_db())
        task = Task(
            title=task_data.title,
            description=task_data.description,
            status=task_data.status
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
