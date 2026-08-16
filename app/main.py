from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(
    title="Cloud Native DevOps Platform",
    version="1.0.0"
)


class Task(BaseModel):
    title: str
    description: str = ""
    completed: bool = False


tasks = {}
next_id = 1


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


@app.get("/api/tasks")
def get_tasks():
    return list(tasks.values())


@app.post("/api/tasks")
def create_task(task: Task):
    global next_id

    new_task = {
        "id": next_id,
        **task.model_dump()
    }

    tasks[next_id] = new_task
    next_id += 1

    return new_task


@app.get("/api/tasks/{task_id}")
def get_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return tasks[task_id]


@app.put("/api/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    if task_id not in tasks:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    updated_task = {
        "id": task_id,
        **task.model_dump()
    }

    tasks[task_id] = updated_task

    return updated_task


@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    deleted_task = tasks.pop(task_id)

    return {
        "message": "Task deleted successfully",
        "task": deleted_task
    }