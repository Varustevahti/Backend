# app/crud.py
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app import models, schemas

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


# Location
def create_location(db: Session, location: schemas.LocationCreate):
    db_loc = models.Location(**location.model_dump())
    db.add(db_loc)
    db.commit()
    db.refresh(db_loc)
    return db_loc


def get_locations(db: Session):
    return db.query(models.Location).order_by(models.Location.name.asc()).all()


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
    return (
        db.query(models.Item)
        .filter(models.Item.category_id == category_id)
        .all()
    )


def get_items_by_group(db: Session, group_id: int):
    return db.query(models.Item).filter(models.Item.group_id == group_id).all()


def get_items_by_location(db: Session, location_id: int):
    return (
        db.query(models.Item)
        .filter(models.Item.location_id == location_id)
        .all()
    )


def update_item(db: Session, item_id: int, item_update: schemas.ItemUpdate):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not db_item:
        return None

    allowed_fields = [
        "name",
        "location",
        "location_id",
        "desc",
        "owner",
        "size",
        "category_id",
        "group_id",
        "price",
        "on_market_place",
        "image",
    ]

    data = item_update.model_dump(exclude_unset=True)
    for key in allowed_fields:
        if key in data:
            setattr(db_item, key, data[key])

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


def get_recent_items(db: Session, limit: int = 10):
    return (
        db.query(models.Item)
        .order_by(desc(models.Item.timestamp))
        .limit(limit)
        .all()
    )


def post_item_to_market(db: Session, item_id: int, price: float):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not db_item:
        return None
    db_item.on_market_place = 1
    db_item.price = price
    db.commit()
    db.refresh(db_item)
    return db_item
