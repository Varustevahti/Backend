# app/crud.py
from sqlalchemy.orm import Session
from app import models, schemas
from sqlalchemy import desc

# --- Helpers: get-or-create by name ---
def get_category_by_name(db: Session, name: str):
    return db.query(models.Category).filter(models.Category.name == name).first()

def get_or_create_category(db: Session, name: str):
    cat = get_category_by_name(db, name)
    if cat:
        return cat
    cat = models.Category(name=name)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat

def get_group_by_name(db: Session, name: str):
    return db.query(models.Group).filter(models.Group.name == name).first()

def get_or_create_group(db: Session, name: str):
    grp = get_group_by_name(db, name)
    if grp:
        return grp
    grp = models.Group(name=name)
    db.add(grp)
    db.commit()
    db.refresh(grp)
    return grp

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

def update_item(db: Session, item_id: int, item_update: schemas.ItemUpdate):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not db_item:
        return None
    allowed_fields = ["name", "location", "owner", "size", "description"]
    for key in allowed_fields:
        if key in item_update.model_dump(exclude_unset=True):
            setattr(db_item, key, getattr(item_update, key))
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not db_item:
        return None
    db.delete(db_item)
    db.commit()
    return db_item

def get_marketplace_items(db: Session):
    return db.query(models.Item).filter(models.Item.on_market_place == 1).all()

def get_recent_items(db: Session, limit: int = 10): #set the limit for how many items you need returned, wasnt sure, so 10 it is. also change this in routers.py if you wanna change it
    return db.query(models.Item).order_by(desc(models.Item.created_at)).limit(limit).all()

def post_item_to_market(db: Session, item_id: int, price: float):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not db_item:
        return None
    db_item.on_market_place = 1
    db_item.price = price
    db.commit()
    db.refresh(db_item)
    return db_item