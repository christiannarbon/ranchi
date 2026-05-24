from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey, func
from datetime import datetime
from typing import List, Optional

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[str] = mapped_column(String)
    daily_status: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    group_members: Mapped[List["GroupMember"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    votes: Mapped[List["Vote"]] = relationship(back_populates="user", cascade="all, delete-orphan")

class Group(Base):
    __tablename__ = "groups"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    is_locked: Mapped[bool] = mapped_column(Boolean, default=False)
    winning_restaurant_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    members: Mapped[List["GroupMember"]] = relationship(back_populates="group", cascade="all, delete-orphan")
    nominations: Mapped[List["Nomination"]] = relationship(back_populates="group", cascade="all, delete-orphan")

class GroupMember(Base):
    __tablename__ = "group_members"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id", ondelete="CASCADE"), index=True)

    user: Mapped["User"] = relationship(back_populates="group_members")
    group: Mapped["Group"] = relationship(back_populates="members")

class Nomination(Base):
    __tablename__ = "nominations"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id", ondelete="CASCADE"), index=True)
    restaurant_name: Mapped[str] = mapped_column(String)
    google_place_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    group: Mapped["Group"] = relationship(back_populates="nominations")
    votes: Mapped[List["Vote"]] = relationship(back_populates="nomination", cascade="all, delete-orphan")

class Vote(Base):
    __tablename__ = "votes"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    nomination_id: Mapped[int] = mapped_column(ForeignKey("nominations.id", ondelete="CASCADE"), index=True)

    user: Mapped["User"] = relationship(back_populates="votes")
    nomination: Mapped["Nomination"] = relationship(back_populates="votes")
