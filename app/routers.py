# app/routers.py
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, Header
from sqlalchemy.orm import Session
from app import crud, models, schemas, database

from PIL import Image
import io
import traceback

# AI-malli (label packs + CLIP)
from AI_Model.demo_app_zeroshot import classify_pil, save_upload

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---- current user via headers from frontend (Clerk) ----
def current_user(
    db: Session = Depends(get_db),
    x_user_id: str = Header(None, convert_underscores=False),
    x_user_email: str = Header(None, convert_underscores=False),
    x_user_name: str = Header(None, convert_underscores=False),
):
    # Selkeä debug kaikista otsakkeista
    print(
        f"AUTH DEBUG -> method: (via Depends current_user) | "
        f"uid: {x_user_id} | email: {x_user_email} | name: {x_user_name}"
    )
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Missing X-User-Id")

    # Upsert varmistaa että käyttäjä on tietokannassa
    user = crud.upsert_user(
        db,
        schemas.UserUpsert(
            clerk_id=x_user_id,
            email=x_user_email,
            name=x_user_name,
        ),
    )
    return user

# --- Auto classify + create ---
@router.post("/items/auto", response_model=schemas.ItemModel)
async def create_item_auto(
    file: UploadFile = File(...),
    # NIMEÄ EI ENÄÄ OTETA FRONTILTA — backend asettaa aina nimen
    location: str | None = Form(None),
    location_id: int | None = Form(None),
    db: Session = Depends(get_db),
    user: models.User = Depends(current_user),
):
    """
    Vastaanottaa yhden kuvan, luokittelee sen CLIPillä ja luo Itemin.
    - Nimi asetetaan aina mallin parhaasta labelista -> ei voi olla None.
    - Kuva tallennetaan /uploads -kansioon (save_upload).
    - Category ja Group luodaan/haetaan pack-nimen mukaan.
    """
    # Hyvin selkeä debug alkudatasta
    try:
        print(f"ITEMS/AUTO DEBUG -> user: {{'id': '{user.clerk_id}', 'email': '{user.email}', 'name': '{user.name}'}}")
    except Exception:
        pass

    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(status_code=415, detail="Only image uploads are supported.")

    try:
        # 1) Lue bytes ja tallenna kuva levylle
        content = await file.read()
        filename = getattr(file, "filename", "upload.jpg")
        image_path = save_upload(content, upload_dir="uploads")
        print(f"ITEMS/AUTO DEBUG -> fields: location_id: {location_id} | filename: {filename}")
        print(f"ITEMS/AUTO DEBUG -> saved image to: {image_path}")

        # 2) Luokittelu
        img = Image.open(io.BytesIO(content)).convert("RGB")
        best_label, prob, pack, _topk = classify_pil(img, topk=5)
        print(f"ITEMS/AUTO DEBUG -> CLIP best_label='{best_label}', prob={prob:.4f}, pack='{pack}'")

        # Varmista että best_label on aina järkevä merkkijono
        safe_label = (best_label or "").strip() or "Detected item"

        # 3) Hae/luo Category + Group paketin nimellä (pack)
        #    Jos pack on tyhjä, käytä 'Unknown' ettei jää Noneksi
        safe_pack = (pack or "").strip() or "Unknown"
        cat = crud.get_or_create_category(db, safe_pack)
        grp = crud.get_or_create_group(db, safe_pack)
        print(f"ITEMS/AUTO DEBUG -> mapped pack='{safe_pack}' -> category_id={cat.id if cat else None}, group_id={grp.id if grp else None}")

        # 4) Luo Item.
        #    HUOM: name asetetaan aina safe_label -> vastaa NOT NULL -rajoitetta.
        #    desc asetetaan myös safe_label (näkyy kivasti UI:ssa).
        item_in = schemas.ItemBase(
            name=safe_label,
            desc=safe_label,
            image=image_path,
            owner=user.clerk_id,               # owner = Clerk user id
            location=location or None,
            location_id=location_id if location_id is not None else None,
            category_id=cat.id if cat else None,
            group_id=grp.id if grp else None,
        )
        print(f"ITEMS/AUTO DEBUG -> will create item: {item_in}")

        created = crud.create_item(db, item_in)
        print(f"ITEMS/AUTO DEBUG -> created item id={created.id}")
        return created

    except HTTPException:
        raise
    except Exception as e:
        # Printataan koko stacktrace selvittelyn helpottamiseksi
        tb = traceback.format_exc()
        print("ITEMS/AUTO ERROR ->", tb)
        raise HTTPException(status_code=400, detail=f"Classification failed: {e}")

# ---- Muut reitit ----

@router.post("/items/", response_model=schemas.ItemModel)
def create_item(item: schemas.ItemBase, db: Session = Depends(get_db), user: models.User = Depends(current_user)):
    # Varmista että owner on aina kirjautunut käyttäjä
    item.owner = user.clerk_id
    # Jos client ei antaisi nimeä (ei pitäisi käydä), pudotetaan varmuusnimi
    if not (item.name or "").strip():
        item.name = (item.desc or "").strip() or "Unnamed item"
    return crud.create_item(db, item)

@router.get("/items/", response_model=list[schemas.ItemModel])
def get_items(db: Session = Depends(get_db), user: models.User = Depends(current_user)):
    return crud.get_items_for_owner(db, owner_clerk_id=user.clerk_id)

@router.patch("/items/{item_id}", response_model=schemas.ItemModel)
def patch_item(item_id: int, patch: schemas.ItemUpdate, db: Session = Depends(get_db)):
    updated = crud.update_item(db, item_id, patch)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated

@router.get("/items/category/{category_id}", response_model=list[schemas.ItemModel])
def get_items_by_category(category_id: int, db: Session = Depends(get_db), user: models.User = Depends(current_user)):
    return crud.get_items_by_category_for_owner(db, category_id, owner_clerk_id=user.clerk_id)

@router.get("/items/group/{group_id}", response_model=list[schemas.ItemModel])
def get_items_by_group(group_id: int, db: Session = Depends(get_db), user: models.User = Depends(current_user)):
    return crud.get_items_by_group_for_owner(db, group_id, owner_clerk_id=user.clerk_id)

@router.get("/items/by_location/{loc_id}", response_model=list[schemas.ItemModel])
def items_by_location(loc_id: int, db: Session = Depends(get_db), user: models.User = Depends(current_user)):
    return crud.get_items_by_location_for_owner(db, loc_id, owner_clerk_id=user.clerk_id)

# --- Categories ---
@router.post("/categories/", response_model=schemas.CategoryModel)
def create_category(category: schemas.CategoryBase, db: Session = Depends(get_db)):
    return crud.create_category(db, category)

@router.get("/categories/", response_model=list[schemas.CategoryModel])
def get_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)

# ---- Groups ----
@router.post("/groups/", response_model=schemas.GroupModel)
def api_create_group(group: schemas.GroupBase, db: Session = Depends(get_db), user: models.User = Depends(current_user)):
    return crud.create_group(db, owner=user, name=group.name)

@router.get("/groups/my", response_model=list[schemas.GroupModel])
def api_my_groups(db: Session = Depends(get_db), user: models.User = Depends(current_user)):
    return crud.list_user_groups(db, user)

@router.get("/groups/{group_id}/members", response_model=list[schemas.GroupMemberModel])
def api_group_members(group_id: int, db: Session = Depends(get_db), user: models.User = Depends(current_user)):
    return crud.group_members(db, group_id)

@router.post("/groups/{group_id}/invite", response_model=schemas.GroupInviteModel)
def api_invite(group_id: int, invite: schemas.GroupInviteCreate, db: Session = Depends(get_db), user: models.User = Depends(current_user)):
    # only owner can invite
    members = crud.group_members(db, group_id)
    me = next((m for m in members if m.user_id == user.id), None)
    if not me or me.role != "owner":
        raise HTTPException(status_code=403, detail="Only owner can invite")
    grp = db.query(models.Group).filter(models.Group.id == group_id).first()
    if not grp:
        raise HTTPException(status_code=404, detail="Group not found")
    return crud.invite_to_group(db, grp, invite.email)

# --- Locations ---
@router.get("/locations/", response_model=list[schemas.LocationModel])
def get_locations(db: Session = Depends(get_db)):
    return crud.get_locations(db)

@router.post("/locations/", response_model=schemas.LocationModel)
def create_location(loc: schemas.LocationCreate, db: Session = Depends(get_db)):
    return crud.create_location(db, loc)

# Marketplace yms.
@router.get("/items/market", response_model=list[schemas.ItemModel])
def get_marketplace(db: Session = Depends(get_db)):
    return crud.get_marketplace_items(db)

@router.get("/items/recent", response_model=list[schemas.ItemModel])
def get_recent_items(db: Session = Depends(get_db), limit: int = 10):
    return crud.get_recent_items(db, limit=limit)

@router.post("/items/{item_id}/post_to_market", response_model=schemas.ItemModel)
def post_item_to_market(item_id: int, price: float = Form(...), db: Session = Depends(get_db)):
    item = crud.post_item_to_market(db, item_id, price)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item