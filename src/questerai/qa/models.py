import uuid
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector
from questerai.shared.base_model import Base, TimeBaseMixin, UUIDMixin

if TYPE_CHECKING:
    from questerai.interviews.models import Interview
    from questerai.requirements_module.models import QARequirement


class QRecommendation(UUIDMixin, TimeBaseMixin, Base):
    """AI-Recommended Questions generated before or during an interview."""

    __tablename__ = "q_recommendation"

    interview_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("interview.id"),
        nullable=False,
    )
    # The previous turn that triggered this recommendation (nullable for initial turn 0 recommendations)
    source_qa_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("qa.id"),
        nullable=True,
    )

    body: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[str] = mapped_column(String(50), default="discover", nullable=False)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships (singular for single parent)
    interview: Mapped["Interview"] = relationship(back_populates="recommendations")
    source_qa: Mapped["QA | None"] = relationship(
        back_populates="generated_recommendations",
        foreign_keys=[source_qa_id],
    )


class QA(UUIDMixin, TimeBaseMixin, Base):
    """Dialogue Turn recording RE Question, SH Answer, and their vector embeddings."""

    __tablename__ = "qa"

    interview_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("interview.id"),
        nullable=False,
    )
    # Traceability to the AI recommendation chosen by the RE (0..1)
    selected_recommendation_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("q_recommendation.id"),
        nullable=True,
    )

    question: Mapped[str] = mapped_column(Text, nullable=False)
    q_embedding: Mapped[list[float] | None] = mapped_column(Vector(768), nullable=True)
    answer: Mapped[str | None] = mapped_column(Text, nullable=True)
    a_embedding: Mapped[list[float] | None] = mapped_column(Vector(768), nullable=True)
    type: Mapped[str] = mapped_column(String(50), default="open", nullable=False)

    # Relationships (singular for one, plural for many)
    interview: Mapped["Interview"] = relationship(back_populates="qas")
    selected_recommendation: Mapped["QRecommendation | None"] = relationship(
        foreign_keys=[selected_recommendation_id],
    )
    generated_recommendations: Mapped[list["QRecommendation"]] = relationship(
        back_populates="source_qa",
        foreign_keys="[QRecommendation.source_qa_id]",
        cascade="all, delete-orphan",
    )
    qa_requirements: Mapped[list["QARequirement"]] = relationship(
        back_populates="qa",
        cascade="all, delete-orphan",
    )
