# app/models.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

# --- Category ---
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