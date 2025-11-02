# app/crud.py
from sqlalchemy.orm import Session
from app import models, schemas
from sqlalchemy import desc

# ---------- Users ----------
def upsert_user(db: Session, data: schemas.UserUpsert) -> models.User:
    u = db.query(models.User).filter(models.User.clerk_id == data.clerk_id).first()
    if u:
        if data.email:
            u.email = data.email
        if data.name:
            u.name = data.name
    else:
        u = models.User(clerk_id=data.clerk_id, email=data.email, name=data.name)
        db.add(u)
    db.commit()
    db.refresh(u)
    return u

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_clerk_id(db: Session, clerk_id: str):
    return db.query(models.User).filter(models.User.clerk_id == clerk_id).first()



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

# ---------- Group ----------
def create_group(db: Session, owner: models.User, name: str):
    grp = models.Group(name=name)
    db.add(grp)
    db.commit()
    db.refresh(grp)

    gm = models.GroupMember(group_id=grp.id, user_id=owner.id, role="owner")
    db.add(gm)
    db.commit()
    return grp

def list_user_groups(db: Session, user: models.User):
    return (
        db.query(models.Group)
        .join(models.GroupMember, models.Group.id == models.GroupMember.group_id)
        .filter(models.GroupMember.user_id == user.id)
        .all()
    )

def group_members(db: Session, group_id: int):
    return db.query(models.GroupMember).filter(models.GroupMember.group_id == group_id).all()

def invite_to_group(db: Session, group: models.Group, email: str):
    user = get_user_by_email(db, email)
    if user:
        existing = (
            db.query(models.GroupMember)
            .filter(models.GroupMember.group_id == group.id, models.GroupMember.user_id == user.id)
            .first()
        )
        if not existing:
            gm = models.GroupMember(group_id=group.id, user_id=user.id, role="member")
            db.add(gm)
            db.commit()
        inv = models.GroupInvitation(group_id=group.id, email=email, invited_user_id=user.id, status="accepted")
        db.add(inv)
        db.commit()
        db.refresh(inv)
        return inv
    else:
        inv = models.GroupInvitation(group_id=group.id, email=email, invited_user_id=None, status="pending")
        db.add(inv)
        db.commit()
        db.refresh(inv)
        return inv


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

def get_items_for_owner(db: Session, owner_clerk_id: str):
    return db.query(models.Item).filter(models.Item.owner == owner_clerk_id).all()

def get_items_by_category_for_owner(db: Session, category_id: int, owner_clerk_id: str):
    return db.query(models.Item).filter(models.Item.category_id == category_id, models.Item.owner == owner_clerk_id).all()

def get_items_by_group_for_owner(db: Session, group_id: int, owner_clerk_id: str):
    return db.query(models.Item).filter(models.Item.group_id == group_id, models.Item.owner == owner_clerk_id).all()

def get_items_by_location_for_owner(db: Session, loc_id: int, owner_clerk_id: str):
    return db.query(models.Item).filter(models.Item.location_id == loc_id, models.Item.owner == owner_clerk_id).all()