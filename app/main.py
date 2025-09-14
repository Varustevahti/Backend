from fastapi import FastAPI, Depends
from database import SessionLocal, engine
import models
from typing import Annotated, List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins
)

# this entire section will be moved to a dif file once i figure out some things (like routers)
# pydantic models
class ItemBase(BaseModel):
    location: str
    desc: str
    owner: str
    category_id: int
    group_id: int

class CategoryBase(BaseModel):
    name: str

class GroupBase(BaseModel):
    name: str

class ItemModel(ItemBase):
    id: int
    class Config:
        orm_mode = True

class CategoryModel(CategoryBase):
    id: int
    class Config:
        orm_mode = True

class GroupModel(GroupBase):
    id: int
    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

models.Base.metadata.create_all(bind=engine)


# crud endpoints, will be changed once discussed with team what functions are needed, and also moved
# this was purely for testing
'''
@app.post("/items/", response_model=ItemModel)
async def create_item(item: ItemBase, db:db_dependency):
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.post("/categories/", response_model=CategoryModel)
async def create_category(category: CategoryBase, db:db_dependency):
    db_category = models.Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@app.post("/groups/", response_model=GroupModel)
async def create_group(group: GroupBase, db:db_dependency):
    db_group = models.Group(**group.model_dump())
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

@app.get("/items", response_model=List[ItemModel])
async def read_items(db: db_dependency, skip: int = 0):
    items = db.query(models.Item).offset(skip).all()
    return items
'''
@app.get("/items", response_model=List[ItemModel])
async def read_items(db: db_dependency, skip: int = 0):
    items = db.query(models.Item).offset(skip).all()
    return items