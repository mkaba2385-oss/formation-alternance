from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="API Tasks", version="1.0.0")




class TaskCreate(BaseModel):
    titre: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=500)
    priorite: int = Field(ge=1, le=3)


class Task(BaseModel):
    id: int
    titre: str
    description: str
    priorite: int
    terminee: bool = False



tasks: dict[int, Task] = {}

next_id = 1




# GET /tasks
@app.get("/tasks", response_model=list[Task])
def list_tasks() -> list[Task]:
    return list(tasks.values())


# GET /tasks/{id}
@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int) -> Task:
    if task_id not in tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tâche introuvable",
        )

    return tasks[task_id]


# POST /tasks
@app.post(
    "/tasks",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
)
def create_task(data: TaskCreate) -> Task:
    global next_id

    task = Task(
        id=next_id,
        titre=data.titre,
        description=data.description,
        priorite=data.priorite,
    )

    tasks[next_id] = task
    next_id += 1

    return task


# PATCH /tasks/{id}/complete
@app.patch(
    "/tasks/{task_id}/complete",
    response_model=Task,
)
def complete_task(task_id: int) -> Task:
    if task_id not in tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tâche introuvable",
        )

    task = tasks[task_id]

    completed_task = Task(
        id=task.id,
        titre=task.titre,
        description=task.description,
        priorite=task.priorite,
        terminee=True,
    )

    tasks[task_id] = completed_task

    return completed_task


# DELETE /tasks/{id}
@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(task_id: int) -> None:
    if task_id not in tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tâche introuvable",
        )

    del tasks[task_id]