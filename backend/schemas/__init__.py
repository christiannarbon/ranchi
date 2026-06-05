from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Literal


# --- User Schemas ---
class UserBase(BaseModel):
    email: str
    name: str
    daily_status: Optional[str] = None


class UserCreate(UserBase):
    slack_user_id: Optional[str] = None


class UserResponse(UserBase):
    id: int
    api_token: str

    model_config = ConfigDict(from_attributes=True)


class UserPublicResponse(UserBase):
    """User response schema for endpoints that do not need to expose the api_token."""

    id: int

    model_config = ConfigDict(from_attributes=True)


# --- Group Schemas ---
class GroupBase(BaseModel):
    is_locked: bool = False
    winning_restaurant_id: Optional[int] = None


class GroupCreate(GroupBase):
    pass


class GroupResponse(GroupBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --- GroupMember Schemas ---
class GroupMemberBase(BaseModel):
    user_id: int
    group_id: int


class GroupMemberCreate(GroupMemberBase):
    pass


class GroupMemberResponse(GroupMemberBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# --- Nomination Schemas ---
class NominationBase(BaseModel):
    group_id: int
    restaurant_name: str
    google_place_id: Optional[str] = None


class NominationCreate(NominationBase):
    pass


class NominationResponse(NominationBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# --- Vote Schemas ---
class VoteBase(BaseModel):
    user_id: int
    nomination_id: int


class VoteCreate(VoteBase):
    pass


class VoteResponse(VoteBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# --- Request Body Schemas ---


class JoinGroupRequest(BaseModel):
    user_id: int


class NominateRequest(BaseModel):
    user_id: int
    restaurant_name: str
    google_place_id: Optional[str] = None


class VoteRequest(BaseModel):
    user_id: int
    nomination_id: int


class StatusUpdate(BaseModel):
    daily_status: Literal["Looking", "Solo", "Bring Own"]
