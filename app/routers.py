from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Category
@router.post("/categories/", response_model=schemas.CategoryModel)
def create_category(category: schemas.CategoryBase, db: Session = Depends(get_db)):
    return crud.create_category(db, category)

@router.get("/categories/", response_model=list[schemas.CategoryModel])
def get_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)

# Group
@router.post("/groups/", response_model=schemas.GroupModel)
def create_group(group: schemas.GroupBase, db: Session = Depends(get_db)):
    return crud.create_group(db, group)

@router.get("/groups/", response_model=list[schemas.GroupModel])
def get_groups(db: Session = Depends(get_db)):
    return crud.get_groups(db)

# Item
@router.post("/items/", response_model=schemas.ItemModel)
def create_item(item: schemas.ItemBase, db: Session = Depends(get_db)):
    return crud.create_item(db, item)

@router.get("/items/", response_model=list[schemas.ItemModel])
def get_items(db: Session = Depends(get_db)):
    return crud.get_items(db)

@router.get("/items/category/{category_id}", response_model=list[schemas.ItemModel])
def get_items_by_category(category_id: int, db: Session = Depends(get_db)):
    return crud.get_items_by_category(db, category_id)

@router.get("/items/group/{group_id}", response_model=list[schemas.ItemModel])
def get_items_by_group(group_id: int, db: Session = Depends(get_db)):
    return crud.get_items_by_group(db, group_id)
