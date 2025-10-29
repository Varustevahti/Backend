# app/models.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import Column, ForeignKey, String, Integer, Float, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.sql import func

# --- Category ---
# https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#orm-declarative-mapping

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable = False)
    location = Column(String, index=True)
    desc = Column(String)                 # mallitulos (label)
    owner = Column(String)
    image = Column(String, nullable=True) # image file path
    size = Column(String, nullable=True)
    on_market_place = Column(Integer, default=0)           # NEW: 0=not, 1=on market, 2=sold
    price = Column(Float, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    # foreign keys
    category_id = Column(Integer, ForeignKey("categories.id"))
    group_id = Column(Integer, ForeignKey("groups.id"))
    # relationships
    category = relationship("Category", back_populates="items")
    group = relationship("Group", back_populates="items")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    items = relationship("Item", back_populates="category_rel")

# --- Group ---
class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    items = relationship("Item", back_populates="group_rel")

# --- Location ---
class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    owner = Column(String, nullable=True)

    items = relationship("Item", back_populates="location_rel")

# --- Item ---
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    desc = Column(String, nullable=True)           # tunnistettu nimi / kuvaus
    image = Column(String, nullable=True)          # esim. uploads/xxx.jpg
    owner = Column(String, nullable=True)
    location = Column(String, nullable=True)       # legacy string (saa jäädä)

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)

    category_rel = relationship("Category", back_populates="items")
    group_rel = relationship("Group", back_populates="items")
    location_rel = relationship("Location", back_populates="items")