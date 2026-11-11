"""SQLAlchemy models for Requirement and QARequirement (traceability junction) entities."""

import uuid
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector
from questerai.shared.base_model import Base, TimeBaseMixin, UUIDMixin

if TYPE_CHECKING:
    from questerai.qa.models import QA


class Requirement(UUIDMixin, TimeBaseMixin, Base):
    """Software requirement discovered, refined, or validated during interviews."""

    __tablename__ = "requirement"

    requirement: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[str] = mapped_column(String(50), default="functional", nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="draft", nullable=False)
    r_embedding: Mapped[list[float] | None] = mapped_column(Vector(768), nullable=True)

    # Plural because one requirement can trace to many QA dialogue turns
    qa_requirements: Mapped[list["QARequirement"]] = relationship(
        back_populates="requirement",
        cascade="all, delete-orphan",
    )


class QARequirement(UUIDMixin, TimeBaseMixin, Base):
    """Traceability junction entity linking a Requirement to its supporting Q-A dialogue turn."""

    __tablename__ = "qa_requirement"

    requirement_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("requirement.id"),
        nullable=False,
    )
    qa_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("qa.id"),
        nullable=False,
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Singular because each junction row points to ONE requirement and ONE qa turn
    requirement: Mapped["Requirement"] = relationship(back_populates="qa_requirements")
    qa: Mapped["QA"] = relationship(back_populates="qa_requirements")
