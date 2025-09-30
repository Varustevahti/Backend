# app/models.py
from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship
from app.database import Base

# https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#orm-declarative-mapping

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, index=True)
    desc = Column(String)                 # mallitulos (label)
    owner = Column(String)
    image = Column(String, nullable=True) # image file path
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

