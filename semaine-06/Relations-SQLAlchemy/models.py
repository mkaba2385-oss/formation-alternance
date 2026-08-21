from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    books: Mapped[list["Book"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan",
    )


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    isbn: Mapped[str]

    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.id")
    )

    author: Mapped["Author"] = relationship(
        back_populates="books"
    )

    reviews: Mapped[list["Review"]] = relationship(
        back_populates="book",
        cascade="all, delete-orphan",
    )


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    rating: Mapped[int]

    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id")
    )

    book: Mapped["Book"] = relationship(
        back_populates="reviews"
    )