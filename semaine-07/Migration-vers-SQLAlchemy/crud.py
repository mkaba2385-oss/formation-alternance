from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas


def list_tasks(db: Session) -> list[models.Task]:
    stmt = select(models.Task)
    return list(db.scalars(stmt))


def get_task(
    db: Session,
    task_id: int,
) -> models.Task | None:
    return db.get(models.Task, task_id)


def create_task(
    db: Session,
    data: schemas.TaskCreate,
) -> models.Task:
    task = models.Task(**data.model_dump())

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def complete_task(
    db: Session,
    task_id: int,
) -> models.Task | None:
    task = db.get(models.Task, task_id)

    if task is None:
        return None

    task.terminee = True

    db.commit()
    db.refresh(task)

    return task


def delete_task(
    db: Session,
    task_id: int,
) -> bool:
    task = db.get(models.Task, task_id)

    if task is None:
        return False

    db.delete(task)
    db.commit()

    return True