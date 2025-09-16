from pydantic import BaseModel

#Category
class CategoryBase(BaseModel):
    name: str

class CategoryModel(CategoryBase):
    id: int
    class Config:
        orm_mode = True

# Group
class GroupBase(BaseModel):
    name: str

class GroupModel(GroupBase):
    id: int
    class Config:
        orm_mode = True

#Item
class ItemBase(BaseModel):
    location: str
    desc: str
    owner: str
    category_id: int
    group_id: int
    image: str

class ItemModel(ItemBase):
    id: int
    class Config:
        orm_mode = True