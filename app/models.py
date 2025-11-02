# app/models.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import Column, ForeignKey, String, Integer, Float, DateTime, UniqueConstraint
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
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    # relationships
    category_rel = relationship("Category", back_populates="items")
    group_rel = relationship("Group", back_populates="items")
    location_rel = relationship("Location", back_populates="items")

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

    members = relationship("GroupMember", back_populates="group", cascade="all, delete-orphan")
    invitations = relationship("GroupInvitation", back_populates="group", cascade="all, delete-orphan")

    items = relationship("Item", back_populates="group_rel")

# --- Location ---
class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    owner = Column(String, nullable=True)

    items = relationship("Item", back_populates="location_rel")

# --- User (Clerk-peilaus) ---
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    clerk_id = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, index=True, nullable=True)
    name = Column(String, nullable=True)

    memberships = relationship("GroupMember", back_populates="user", cascade="all, delete-orphan")
    invitations = relationship("GroupInvitation", back_populates="invited_user", cascade="all, delete-orphan")

    # --- GroupMember (many-to-many User<->Group) ---
class GroupMember(Base):
    __tablename__ = "group_members"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String, default="member")  # "owner" | "member"

    __table_args__ = (UniqueConstraint("group_id", "user_id", name="uq_group_user"),)

    group = relationship("Group", back_populates="members")
    user = relationship("User", back_populates="memberships")

# --- Invitation (pending or accepted) ---
class GroupInvitation(Base):
    __tablename__ = "group_invitations"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    email = Column(String, nullable=False)
    invited_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(String, default="pending")  # pending | accepted | revoked

    group = relationship("Group", back_populates="invitations")
    invited_user = relationship("User", back_populates="invitations")

