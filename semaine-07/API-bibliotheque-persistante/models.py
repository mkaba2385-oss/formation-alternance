from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    titre: Mapped[str]
    description: Mapped[str]
    priorite: Mapped[int]
    terminee: Mapped[bool] = mapped_column(default=False)