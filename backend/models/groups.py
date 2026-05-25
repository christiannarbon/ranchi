from typing import List, Optional, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import Integer, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

if TYPE_CHECKING:
    from models.users import User
    from models.voting import Nomination


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    is_locked: Mapped[bool] = mapped_column(Boolean, default=False)
    winning_restaurant_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    members: Mapped[List["GroupMember"]] = relationship(
        back_populates="group", cascade="all, delete-orphan"
    )
    nominations: Mapped[List["Nomination"]] = relationship(
        back_populates="group", cascade="all, delete-orphan"
    )


class GroupMember(Base):
    __tablename__ = "group_members"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    group_id: Mapped[int] = mapped_column(
        ForeignKey("groups.id", ondelete="CASCADE"), index=True
    )

    user: Mapped["User"] = relationship(back_populates="group_members")
    group: Mapped["Group"] = relationship(back_populates="members")
