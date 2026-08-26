from datetime import UTC, datetime
from uuid import UUID, uuid4
from models import Session
from session_store import SessionStore


class SessionService:

    def __init__(self, session_store: SessionStore) -> None:
        self.session_store = session_store
        self.revoked_tokens: set[str] = set()

    def create_session(
        self,
        *,
        user_id: str,
        jti: str,
        device_info: str,
    ) -> Session:
        now = datetime.now(UTC)

        session = Session(
            id=uuid4(),
            user_id=user_id,
            jti=jti,
            device_info=device_info,
            created_at=now,
            last_used_at=now,
        )

        self.session_store.add(session)
        return session

    def list_sessions(self, user_id: str) -> list[Session]:
        return self.session_store.get_by_user_id(user_id)

    def revoke_session(
        self,
        *,
        user_id: str,
        session_id: UUID,
    ) -> None:
        session = self.session_store.get_by_id(session_id)

        if session is None:
            raise ValueError("Session introuvable")

        if session.user_id != user_id:
            raise PermissionError("Cette session ne vous appartient pas")

        self.revoked_tokens.add(session.jti)
        self.session_store.delete(session_id)

    def revoke_other_sessions(
        self,
        *,
        user_id: str,
        current_session_id: UUID,
    ) -> None:
        sessions = self.session_store.get_by_user_id(user_id)

        for session in sessions:
            if session.id == current_session_id:
                continue

            self.revoked_tokens.add(session.jti)
            self.session_store.delete(session.id)

    def update_last_used(self, session_id: UUID) -> None:
        session = self.session_store.get_by_id(session_id)

        if session is not None:
            session.last_used_at = datetime.now(UTC)
