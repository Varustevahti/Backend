# app/routers.py
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database

from PIL import Image
import io

# AI-malli (label packs + CLIP)
from AI_Model.demo_app_zeroshot import classify_pil, save_upload

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Auto classify + create ---
@router.post("/items/auto", response_model=schemas.ItemModel)
async def create_item_auto(
    file: UploadFile = File(...),
    name: str = Form(...),
    owner: str = Form(""),
    location: str | None = Form(None),            
    location_id: int | None = Form(None),         # valinnainen, jos user valinnut
    db: Session = Depends(get_db),
):
    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(status_code=415, detail="Only image uploads are supported.")

    try:
        # 1) Tallenna kuva levylle
        content = await file.read()
        image_path = save_upload(content, upload_dir="uploads")

        # 2) Luokittelu
        img = Image.open(io.BytesIO(content)).convert("RGB")
        best_label, prob, pack, _topk = classify_pil(img, topk=5)

        # 3) Hae/luo Category + Group paketin nimellä (pack)
        cat = crud.get_or_create_category(db, pack)
        grp = crud.get_or_create_group(db, pack)

        # 4) Luo Item
        item_in = schemas.ItemBase(
            name=name,
            location=location,
            desc=best_label,
            image=image_path,
            owner=owner or None,
            location=location or None,
            location_id=location_id if location_id is not None else None,
            category_id=cat.id,
            group_id=grp.id,
        )
        created = crud.create_item(db, item_in)
        return created

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Classification failed: {e}")

# --- Items: list & update ---
@router.get("/items/", response_model=list[schemas.ItemModel])
def get_items(db: Session = Depends(get_db)):
    return crud.get_items(db)

@router.patch("/items/{item_id}", response_model=schemas.ItemModel)
def patch_item(item_id: int, patch: schemas.ItemUpdate, db: Session = Depends(get_db)):
    updated = crud.update_item(db, item_id, patch)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated

@router.get("/items/category/{category_id}", response_model=list[schemas.ItemModel])
def get_items_by_category(category_id: int, db: Session = Depends(get_db)):
    return crud.get_items_by_category(db, category_id)

@router.get("/items/group/{group_id}", response_model=list[schemas.ItemModel])
def get_items_by_group(group_id: int, db: Session = Depends(get_db)):
    return crud.get_items_by_group(db, group_id)

@router.get("/items/by_location/{loc_id}", response_model=list[schemas.ItemModel])
def items_by_location(loc_id: int, db: Session = Depends(get_db)):
    return crud.get_items_by_location(db, loc_id)

# --- Categories ---
@router.post("/categories/", response_model=schemas.CategoryModel)
def create_category(category: schemas.CategoryBase, db: Session = Depends(get_db)):
    return crud.create_category(db, category)

@router.get("/categories/", response_model=list[schemas.CategoryModel])
def get_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)

# --- Groups ---
@router.post("/groups/", response_model=schemas.GroupModel)
def create_group(group: schemas.GroupBase, db: Session = Depends(get_db)):
    return crud.create_group(db, group)

@router.get("/groups/", response_model=list[schemas.GroupModel])
def get_groups(db: Session = Depends(get_db)):
    return crud.get_groups(db)

# --- Locations ---
@router.get("/locations/", response_model=list[schemas.LocationModel])
def get_locations(db: Session = Depends(get_db)):
    return crud.get_locations(db)

@router.post("/locations/", response_model=schemas.LocationModel)
def create_location(loc: schemas.LocationCreate, db: Session = Depends(get_db)):
    return crud.create_location(db, loc)
@router.get("/items/", response_model=list[schemas.ItemModel])
def get_items(db: Session = Depends(get_db)):
    return crud.get_items(db)

@router.get("/items/category/{category_id}", response_model=list[schemas.ItemModel])
def get_items_by_category(category_id: int, db: Session = Depends(get_db)):
    return crud.get_items_by_category(db, category_id)

@router.get("/items/group/{group_id}", response_model=list[schemas.ItemModel])
def get_items_by_group(group_id: int, db: Session = Depends(get_db)):
    return crud.get_items_by_group(db, group_id)

@router.put("/items/{item_id}", response_model=schemas.ItemModel)
def update_item(item_id: int, item_update: schemas.ItemUpdate, db: Session = Depends(get_db)):
    updated = crud.update_item(db, item_id, item_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated

@router.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_item(db, item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"Item deleted"}

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
