"""Declarative Base and common column mixins for all models."""
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
import uuid
import uuid6
from sqlalchemy import DateTime, Boolean, func, Uuid
from datetime import datetime


class Base(DeclarativeBase):
    pass

class TimeBaseMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, index=True)

    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

class UUIDMixin:
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid6.uuid7,
    )
    
