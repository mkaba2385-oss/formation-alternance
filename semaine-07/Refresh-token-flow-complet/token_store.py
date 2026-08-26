class TokenStore:
    """Simulation d'un stockage Redis."""

    def __init__(self) -> None:
        self.revoked_tokens: set[str] = set()
        self.user_tokens: dict[str, set[str]] = {}

    def add_token(self, user_id: str, jti: str) -> None:
        """Enregistre un token actif pour un utilisateur."""
        if user_id not in self.user_tokens:
            self.user_tokens[user_id] = set()
        self.user_tokens[user_id].add(jti)

    def revoke_token(self, jti: str) -> None:
        """Ajoute un token à la blacklist."""
        self.revoked_tokens.add(jti)

    def is_revoked(self, jti: str) -> bool:
        """Vérifie si un token est révoqué."""
        return jti in self.revoked_tokens

    def revoke_all_user_tokens(self, user_id: str) -> None:
        """Révoque tous les refresh tokens d'un utilisateur."""
        tokens = self.user_tokens.get(user_id, set())
        for jti in tokens:
            self.revoked_tokens.add(jti)
        self.user_tokens[user_id] = set()
