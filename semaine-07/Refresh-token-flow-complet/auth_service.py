from security import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from token_store import TokenStore


class AuthService:

    def __init__(self, token_store: TokenStore) -> None:
        self.token_store = token_store

    def login(self, user_id: str) -> dict[str, str]:
        """Simule une connexion utilisateur."""
        access_token = create_access_token(user_id)
        refresh_token = create_refresh_token(user_id)

        payload = decode_token(refresh_token)
        jti = str(payload["jti"])

        self.token_store.add_token(user_id, jti)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    def refresh(self, refresh_token: str) -> dict[str, str]:
        """Vérifie un refresh token, invalide l'ancien et crée une nouvelle paire."""
        payload = decode_token(refresh_token)

        token_type = payload.get("type")
        if token_type != "refresh":
            raise ValueError("Le token doit être un refresh token")

        user_id = payload.get("sub")
        jti = payload.get("jti")

        if not user_id or not jti:
            raise ValueError("Refresh token invalide")

        user_id = str(user_id)
        jti = str(jti)

        if self.token_store.is_revoked(jti):
            self.token_store.revoke_all_user_tokens(user_id)
            raise ValueError(
                "Refresh token déjà utilisé. Toutes les sessions ont été révoquées."
            )

        self.token_store.revoke_token(jti)

        new_access_token = create_access_token(user_id)
        new_refresh_token = create_refresh_token(user_id)

        new_payload = decode_token(new_refresh_token)
        new_jti = str(new_payload["jti"])

        self.token_store.add_token(user_id, new_jti)

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
        }
