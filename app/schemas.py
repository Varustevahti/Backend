# app/schemas.py
from typing import Optional, List
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ---- Users ----
class UserUpsert(BaseModel):
    clerk_id: str
    email: Optional[str] = None
    name: Optional[str] = None

class UserModel(UserUpsert):
    id: int
    class Config:
        from_attributes = True

# --- Category ---
class CategoryBase(BaseModel):
    name: str

class CategoryModel(CategoryBase):
    id: int
    class Config:
        from_attributes = True

# --- Group ---
class GroupBase(BaseModel):
    name: str

class GroupModel(GroupBase):
    id: int
    class Config:
        from_attributes = True

class GroupMemberModel(BaseModel):
    id: int
    group_id: int
    user_id: int
    role: str = "member"
    class Config:
        from_attributes = True

class GroupInviteCreate(BaseModel):
    email: str

class GroupInviteModel(BaseModel):
    id: int
    group_id: int
    email: str
    invited_user_id: Optional[int] = None
    status: str
    class Config:
        from_attributes = True


# --- Location ---
class LocationBase(BaseModel):
    name: str
    description: Optional[str] = None
    owner: Optional[str] = None

class LocationCreate(LocationBase):
    pass

class LocationModel(LocationBase):
    id: int
    class Config:
        from_attributes = True

# --- Item ---
class ItemBase(BaseModel):
    desc: Optional[str] = None
    image: Optional[str] = None
    category_id: Optional[int] = None
    group_id: Optional[int] = None
    owner: Optional[str] = None
    location: Optional[str] = None         
    location_id: Optional[int] = None

    class Config:
        from_attributes = True

class ItemModel(ItemBase):
    id: int
    class Config:
        from_attributes = True

class ItemUpdate(BaseModel):
    desc: Optional[str] = None
    category_id: Optional[int] = None
    location_id: Optional[int] = None
    owner: Optional[str] = None
    name: Optional[str] = None
    location: Optional[str] = None
    desc: Optional[str] = None
    owner: Optional[str] = None
    category_id: Optional[int] = None
    group_id: Optional[int] = None
    image: Optional[str] = None
    size: Optional[str] = None
    on_market_place: Optional[int] = None
    price: Optional[float] = None



