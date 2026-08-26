from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Session:
    id: UUID
    user_id: str
    jti: str
    device_info: str
    created_at: datetime
    last_used_at: datetime
