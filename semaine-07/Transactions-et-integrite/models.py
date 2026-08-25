from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    titre: Mapped[str]
    description: Mapped[str]
    priorite: Mapped[int]
    terminee: Mapped[bool] = mapped_column(default=False)


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str]
    stock: Mapped[int]


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id")
    )
    quantity: Mapped[int]