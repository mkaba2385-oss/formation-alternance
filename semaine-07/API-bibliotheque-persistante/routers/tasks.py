from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..db import get_db

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.get(
    "",
    response_model=list[schemas.TaskOut],
)
def list_tasks(
    db: Session = Depends(get_db),
) -> list[schemas.TaskOut]:
    return crud.list_tasks(db)


@router.get(
    "/{task_id}",
    response_model=schemas.TaskOut,
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
) -> schemas.TaskOut:
    task = crud.get_task(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tâche introuvable",
        )

    return task


@router.post(
    "",
    response_model=schemas.TaskOut,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    data: schemas.TaskCreate,
    db: Session = Depends(get_db),
) -> schemas.TaskOut:
    return crud.create_task(db, data)


@router.patch(
    "/{task_id}/complete",
    response_model=schemas.TaskOut,
)
def complete_task(
    task_id: int,
    db: Session = Depends(get_db),
) -> schemas.TaskOut:
    task = crud.complete_task(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tâche introuvable",
        )

    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
) -> None:
    deleted = crud.delete_task(db, task_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tâche introuvable",
        )