# app/crud.py
from sqlalchemy.orm import Session
from app import models, schemas

# --- helpers: get-or-create by name ---
def get_category_by_name(db: Session, name: str):
    return db.query(models.Category).filter(models.Category.name == name).first()

def get_or_create_category(db: Session, name: str) -> models.Category:
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

def get_or_create_group(db: Session, name: str) -> models.Group:
    grp = get_group_by_name(db, name)
    if grp:
        return grp
    grp = models.Group(name=name)
    db.add(grp)
    db.commit()
    db.refresh(grp)
    return grp

# --- Category ---
def create_category(db: Session, category: schemas.CategoryBase):
    db_cat = models.Category(**category.model_dump())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

def get_categories(db: Session):
    return db.query(models.Category).all()

# --- Group ---
def create_group(db: Session, group: schemas.GroupBase):
    db_group = models.Group(**group.model_dump())
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def get_groups(db: Session):
    return db.query(models.Group).all()

# --- Location ---
def get_locations(db: Session):
    return db.query(models.Location).all()

def create_location(db: Session, loc: schemas.LocationCreate):
    new_loc = models.Location(name=loc.name, description=loc.description, owner=loc.owner)
    db.add(new_loc)
    db.commit()
    db.refresh(new_loc)
    return new_loc

# --- Item ---
def create_item(db: Session, item: schemas.ItemBase):
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_id: int, patch: schemas.ItemUpdate):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not db_item:
        return None
    data = patch.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(db_item, k, v)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_items(db: Session):
    return db.query(models.Item).all()

def get_items_by_category(db: Session, category_id: int):
    return db.query(models.Item).filter(models.Item.category_id == category_id).all()

def get_items_by_group(db: Session, group_id: int):
    return db.query(models.Item).filter(models.Item.group_id == group_id).all()

def get_items_by_location(db: Session, loc_id: int):
    return db.query(models.Item).filter(models.Item.location_id == loc_id).all()