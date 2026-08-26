from uuid import UUID
from models import Session


class SessionStore:

    def __init__(self) -> None:
        self.sessions: dict[UUID, Session] = {}

    def add(self, session: Session) -> None:
        self.sessions[session.id] = session

    def get_by_id(self, session_id: UUID) -> Session | None:
        return self.sessions.get(session_id)

    def get_by_user_id(self, user_id: str) -> list[Session]:
        return [
            session
            for session in self.sessions.values()
            if session.user_id == user_id
        ]

    def delete(self, session_id: UUID) -> None:
        self.sessions.pop(session_id, None)
