from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from main import (
    create_data,
    display_positive_reviews,
    get_authors_with_reviews,
)
from models import Base


def test_display_uses_one_query(
    capsys,
) -> None:
    engine = create_engine("sqlite:///:memory:")

    Base.metadata.create_all(engine)

    with Session(engine) as session:
        create_data(session)

        authors = get_authors_with_reviews(session)

        query_count = 0

        def count_queries(
            conn: object,
            cursor: object,
            statement: str,
            parameters: object,
            context: object,
            executemany: bool,
        ) -> None:
            nonlocal query_count

            if statement.lstrip().upper().startswith("SELECT"):
                query_count += 1

        event.listen(
            engine,
            "before_cursor_execute",
            count_queries,
        )

        display_positive_reviews(authors)

    captured = capsys.readouterr()

    assert "George Orwell: 3 reviews positives" in captured.out
    assert "J. K. Rowling: 3 reviews positives" in captured.out
    assert "Victor Hugo: 1 reviews positives" in captured.out

    assert query_count == 0