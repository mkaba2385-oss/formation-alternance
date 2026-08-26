from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from auth_service import AuthService
from token_store import TokenStore

app = FastAPI(title="Exercise 1 - Refresh Token")

token_store = TokenStore()
auth_service = AuthService(token_store)


class LoginRequest(BaseModel):
    user_id: str


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


@app.post("/auth/login", response_model=TokenResponse)
def login(data: LoginRequest) -> TokenResponse:
    """Endpoint de démonstration pour obtenir une première paire de tokens."""
    tokens = auth_service.login(data.user_id)
    return TokenResponse(**tokens)


@app.post("/auth/refresh", response_model=TokenResponse)
def refresh(data: RefreshRequest) -> TokenResponse:
    """Reçoit un refresh token et retourne une nouvelle paire de tokens."""
    try:
        tokens = auth_service.refresh(data.refresh_token)
        return TokenResponse(**tokens)
    except ValueError as exc:
        raise HTTPException(
            status_code=401,
            detail=str(exc),
        ) from exc
