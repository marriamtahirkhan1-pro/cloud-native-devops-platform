from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Task as TaskModel


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Cloud Native DevOps Platform",
    version="1.0.0"
)


class TaskCreate(BaseModel):
    title: str
    description: str = ""
    completed: bool = False


class TaskResponse(TaskCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "task-api"
    }


@app.get("/")
def root():
    return {
        "message": "Cloud Native DevOps Platform API"
    }


@app.get("/api/tasks", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(TaskModel).all()


@app.post("/api/tasks", response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    new_task = TaskModel(
        title=task.title,
        description=task.description,
        completed=task.completed
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@app.get("/api/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.query(TaskModel).filter(
        TaskModel.id == task_id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


@app.put("/api/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskCreate,
    db: Session = Depends(get_db)
):
    task = db.query(TaskModel).filter(
        TaskModel.id == task_id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task.title = task_data.title
    task.description = task_data.description
    task.completed = task_data.completed

    db.commit()
    db.refresh(task)

    return task


@app.delete("/api/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.query(TaskModel).filter(
        TaskModel.id == task_id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted successfully",
        "task_id": task_id
    }