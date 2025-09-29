from sqlalchemy import Column, ForeignKey, String, Integer, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from app.database import Base

#https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#orm-declarative-mapping
# more constraints will be added, but gotta ponder a bit on that

class Item(Base):
    __tablename__="items"
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, index=True)
    desc = Column(String)
    owner = Column(String)
    image = Column(String, nullable= True) #image file path
    # foreignkeys
    category_id = Column(Integer, ForeignKey("categories.id"))
    group_id = Column(Integer, ForeignKey("groups.id"))
    # relationshiops
    category = relationship("Category", back_populates="items")
    group = relationship("Group", back_populates="items")

class Category(Base):
    __tablename__="categories"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    # relationships
    items = relationship("Item", back_populates="category")

class Group(Base):
    __tablename__="groups"
    id = Column(Integer, primary_key=True)
    name = (String)
    # relationships
    items = relationship("Item", back_populates="group")

#all written assuming: object has one category and one group, and can't have anymore. Owner is also stored as a string for now, instead of being its own class (not sure we'll need it)
