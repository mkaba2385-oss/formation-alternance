from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import Book, Isbn


engine = create_engine("sqlite:///books.db")


def create_book(
    session: Session,
    title: str,
    isbn: str,
) -> Book:
    book = Book(
        title=title,
    )

    book.isbns.append(
        Isbn(isbn=isbn)
    )

    session.add(book)
    session.commit()

    return book


if __name__ == "__main__":
    with Session(engine) as session:
        book = create_book(
            session=session,
            title="Le Hobbit",
            isbn="9780261103344",
        )

        print(f"Livre : {book.title}")

        for isbn_item in book.isbns:
            print(f"ISBN : {isbn_item.isbn}")