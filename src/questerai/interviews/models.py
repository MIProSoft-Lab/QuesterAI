import uuid
from sqlalchemy import ForeignKey, Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from questerai.shared.base_model import Base, TimeBaseMixin, UUIDMixin
from pgvector.sqlalchemy import Vector
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from questerai.projects.models import Project
    from questerai.qa.models import QA, QRecommendation

class Interview(UUIDMixin, TimeBaseMixin, Base):
    __tablename__ = "interview"
    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False,
    )
    project: Mapped["Project"] = relationship(back_populates="interviews")
    sum_embedding: Mapped[list[float] | None] = mapped_column(
        Vector(768)
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    qas: Mapped[list["QA"]] = relationship(
        back_populates="interview",
        cascade="all, delete-orphan",
    )
    recommendations: Mapped[list["QRecommendation"]] = relationship(
        back_populates="interview",
        cascade="all, delete-orphan",
    )