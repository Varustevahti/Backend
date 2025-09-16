from sqlalchemy.orm import Session
from app import models, schemas

# Category
def create_category(db: Session, category: schemas.CategoryBase):
    db_cat = models.Category(**category.model_dump())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

def get_categories(db: Session):
    return db.query(models.Category).all()

# Group
def create_group(db: Session, group: schemas.GroupBase):
    db_group = models.Group(**group.model_dump())
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def get_groups(db: Session):
    return db.query(models.Group).all()
# Item
def create_item(db: Session, item: schemas.ItemBase):
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_items(db: Session):
    return db.query(models.Item).all()

def get_items_by_category(db: Session, category_id: int):
    return db.query(models.Item).filter(models.Item.category_id == category_id).all()

def get_items_by_group(db: Session, group_id: int):
    return db.query(models.Item).filter(models.Item.group_id == group_id).all()