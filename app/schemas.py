# app/schemas.py
from typing import Optional
from pydantic import BaseModel

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

class ItemUpdate(BaseModel):
    desc: Optional[str] = None
    category_id: Optional[int] = None
    location_id: Optional[int] = None
    owner: Optional[str] = None