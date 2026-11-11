"""SQLAlchemy models for Requirement and QARequirement (junction) entities."""
import uuid
from sqlalchemy import ForeignKey, Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from questerai.shared.base_model import Base, TimeBaseMixin, UUIDMixin
from pgvector.sqlalchemy import Vector
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from questerai.qa.models import QA
    

class requirement(UUIDMixin, TimeBaseMixin, Base):
    __tablename__="requirement"
    requirement: Mapped[str] = mapped_column(Text, nullable=False)
    type_req: Mapped[str] = mapped_column(String(50),default="funcional", nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="draft", nullable=False)
    req_embedding: Mapped[list[float]|None] = mapped_column(Vector(768), nullable=True)
    #relationships
    qa_requirements: Mapped[list["qa_requirement"]] = relationship(
        back_populates="requirement",
        cascade="all, delete-orphan",
    )
    



class qa_requirement(UUIDMixin, TimeBaseMixin, Base):
    __tablename__ = "qa_requirement"
    id_req: Mapped[uuid.UUID] = mapped_column(ForeignKey("requirement.id_req"))
    id_qa: Mapped[uuid.UUID] = mapped_column(ForeignKey("qa.id_qa"))
    notes: Mapped[str|None] = mapped_column(Text, nullable=True)
    #relationships
    requirement: Mapped["requirement"] = relationship(back_populates="qa_requirement")
    qa: Mapped["qa"] = relationship(back_populates="qa_requirement")