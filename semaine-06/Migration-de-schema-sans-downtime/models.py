from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]

    isbns: Mapped[list["Isbn"]] = relationship(
        back_populates="book",
        cascade="all, delete-orphan",
    )


class Isbn(Base):
    __tablename__ = "isbns"

    id: Mapped[int] = mapped_column(primary_key=True)
    isbn: Mapped[str]

    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id"),
    )

    book: Mapped["Book"] = relationship(
        back_populates="isbns",
    )