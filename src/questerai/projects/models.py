from typing import TYPE_CHECKING
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from questerai.shared.base_model import Base, TimeBaseMixin, UUIDMixin

if TYPE_CHECKING:
    from questerai.interviews.models import Interview


class Project(UUIDMixin, TimeBaseMixin, Base):
    __tablename__ = "project"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="active", nullable=False)

    interviews: Mapped[list["Interview"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
    )
