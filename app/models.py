# app/models.py
from sqlalchemy import Column, ForeignKey, String, Integer, Float, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.sql import func

# https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#orm-declarative-mapping

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable = False)
    location = Column(String, index=True)
    desc = Column(String)                 # mallitulos (label)
    owner = Column(String, nullable=False) #Yhdistetään tähän clerkin user_id
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
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    items = relationship("Item", back_populates="category")

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)  # <-- KORJATTU
    items = relationship("Item", back_populates="group")

