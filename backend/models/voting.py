from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

if TYPE_CHECKING:
    from models.groups import Group
    from models.users import User


class Nomination(Base):
    __tablename__ = "nominations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    group_id: Mapped[int] = mapped_column(
        ForeignKey("groups.id", ondelete="CASCADE"), index=True
    )
    restaurant_name: Mapped[str] = mapped_column(String)
    google_place_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    group: Mapped["Group"] = relationship(back_populates="nominations")
    votes: Mapped[List["Vote"]] = relationship(
        back_populates="nomination", cascade="all, delete-orphan"
    )


class Vote(Base):
    __tablename__ = "votes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    nomination_id: Mapped[int] = mapped_column(
        ForeignKey("nominations.id", ondelete="CASCADE"), index=True
    )

    user: Mapped["User"] = relationship(back_populates="votes")
    nomination: Mapped["Nomination"] = relationship(back_populates="votes")
