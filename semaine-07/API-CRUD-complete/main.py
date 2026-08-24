from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="API Tasks",
    version="1.0.0",
)




class TaskCreate(BaseModel):
    titre: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=500)
    priorite: int = Field(ge=1, le=3)


class TaskPut(BaseModel):
    titre: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=500)
    priorite: int = Field(ge=1, le=3)
    terminee: bool


class TaskPatch(BaseModel):
    titre: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    description: str | None = Field(
        default=None,
        min_length=1,
        max_length=500,
    )
    priorite: int | None = Field(
        default=None,
        ge=1,
        le=3,
    )
    terminee: bool | None = None


class Task(BaseModel):
    id: int
    titre: str
    description: str
    priorite: int
    terminee: bool = False



tasks: dict[int, Task] = {}

next_id = 1




@app.get("/tasks", response_model=list[Task])
def list_tasks() -> list[Task]:
    return list(tasks.values())





@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int) -> Task:
    if task_id not in tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tâche introuvable",
        )

    return tasks[task_id]




@app.post(
    "/tasks",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
)
def create_task(data: TaskCreate) -> Task:
    global next_id

    task = Task(
        id=next_id,
        **data.model_dump(),
    )

    tasks[next_id] = task
    next_id += 1

    return task




@app.put("/tasks/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    data: TaskPut,
) -> Task:
    if task_id not in tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tâche introuvable",
        )

    updated_task = Task(
        id=task_id,
        **data.model_dump(),
    )

    tasks[task_id] = updated_task

    return updated_task





@app.patch("/tasks/{task_id}", response_model=Task)
def patch_task(
    task_id: int,
    data: TaskPatch,
) -> Task:
    if task_id not in tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tâche introuvable",
        )

    task = tasks[task_id]

    updated_data = data.model_dump(
        exclude_unset=True,
    )

    updated_task = task.model_copy(
        update=updated_data,
    )

    tasks[task_id] = updated_task

    return updated_task




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