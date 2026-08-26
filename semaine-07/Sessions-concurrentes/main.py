from uuid import UUID
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from session_service import SessionService
from session_store import SessionStore

app = FastAPI(title="Exercise 2 - Concurrent Sessions")

session_store = SessionStore()
session_service = SessionService(session_store)


class LoginRequest(BaseModel):
    user_id: str
    jti: str
    device_info: str


@app.post("/auth/login")
def login(data: LoginRequest):
    session = session_service.create_session(
        user_id=data.user_id,
        jti=data.jti,
        device_info=data.device_info,
    )

    return {
        "message": "Connexion réussie",
        "session_id": str(session.id),
    }


@app.get("/auth/sessions")
def list_sessions(x_user_id: str = Header(...)):
    sessions = session_service.list_sessions(x_user_id)

    return [
        {
            "id": str(session.id),
            "user_id": session.user_id,
            "device_info": session.device_info,
            "created_at": session.created_at,
            "last_used_at": session.last_used_at,
        }
        for session in sessions
    ]


@app.delete("/auth/sessions/{session_id}")
def delete_session(
    session_id: UUID,
    x_user_id: str = Header(...),
):
    try:
        session_service.revoke_session(
            user_id=x_user_id,
            session_id=session_id,
        )

        return {"message": "Session révoquée avec succès"}

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except PermissionError as exc:
        raise HTTPException(
            status_code=403,
            detail=str(exc),
        ) from exc


@app.delete("/auth/sessions")
def logout_other_devices(
    x_user_id: str = Header(...),
    x_session_id: UUID = Header(...),
):
    session_service.revoke_other_sessions(
        user_id=x_user_id,
        current_session_id=x_session_id,
    )

    return {"message": "Tous les autres appareils ont été déconnectés"}
