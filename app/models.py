from sqlalchemy import String, Text, Boolean, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from .database import Base


class Message(Base):
    __tablename__ = "message"

    # id for prototype purposes, replace with uuid
    id: Mapped[int] = mapped_column(primary_key=True)

    recipient_id: Mapped[str] = mapped_column(String, index=True, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, index=True
    )
    is_read: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, index=True
    )
