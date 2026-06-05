import uuid
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

if TYPE_CHECKING:
    from models.groups import GroupMember
    from models.voting import Vote


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[str] = mapped_column(String)
    daily_status: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    slack_user_id: Mapped[Optional[str]] = mapped_column(
        String, nullable=True, unique=True
    )
    api_token: Mapped[str] = mapped_column(
        String, unique=True, index=True, default=lambda: str(uuid.uuid4())
    )

    group_members: Mapped[List["GroupMember"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    votes: Mapped[List["Vote"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
