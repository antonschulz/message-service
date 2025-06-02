from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class MessageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    recipient_id: str
    body: str
    created_at: datetime
    is_read: bool


class MessageDeleteMultiple(BaseModel):
    message_ids: List[int]
