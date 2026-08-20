from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, selectinload

from models import Author, Base, Book, Review


engine = create_engine("sqlite:///library.db")


def create_data(session: Session) -> None:
    authors = [
        Author(name="George Orwell"),
        Author(name="J. K. Rowling"),
        Author(name="Victor Hugo"),
    ]

    books = [
        Book(title="1984", author=authors[0]),
        Book(title="Animal Farm", author=authors[0]),
        Book(title="Harry Potter 1", author=authors[1]),
        Book(title="Harry Potter 2", author=authors[1]),
        Book(title="Les Miserables", author=authors[2]),
    ]

    reviews = [
        Review(rating=5, book=books[0]),
        Review(rating=4, book=books[0]),
        Review(rating=3, book=books[1]),
        Review(rating=5, book=books[1]),
        Review(rating=4, book=books[2]),
        Review(rating=5, book=books[2]),
        Review(rating=2, book=books[3]),
        Review(rating=4, book=books[3]),
        Review(rating=5, book=books[4]),
        Review(rating=3, book=books[4]),
    ]

    session.add_all(authors)
    session.add_all(books)
    session.add_all(reviews)

    session.commit()


def get_authors_with_reviews(session: Session) -> list[Author]:
    stmt = select(Author).options(
        selectinload(Author.books).selectinload(Book.reviews)
    )

    return session.scalars(stmt).all()


def display_positive_reviews(authors: list[Author]) -> None:
    for author in authors:
        positive_reviews = sum(
            1
            for book in author.books
            for review in book.reviews
            if review.rating >= 4
        )

        print(
            f"{author.name}: "
            f"{positive_reviews} reviews positives"
        )


def main() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        create_data(session)

    with Session(engine) as session:
        authors = get_authors_with_reviews(session)
        display_positive_reviews(authors)


if __name__ == "__main__":
    main()