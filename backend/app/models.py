from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Dish(Base):
    __tablename__ = "dishes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    category = Column(String(50))
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    orders = relationship("Order", back_populates="dish")
    __table_args__ = (CheckConstraint("price >= 0", name="check_price_positive"),)


class Table(Base):
    __tablename__ = "tables"
    id = Column(Integer, primary_key=True, index=True)
    table_number = Column(String(10), nullable=False, unique=True)
    capacity = Column(Integer, default=4)
    status = Column(String(20), default="available")
    created_at = Column(DateTime, server_default=func.now())
    orders = relationship("Order", back_populates="table")
    __table_args__ = (
        CheckConstraint("capacity > 0", name="check_capacity_positive"),
        CheckConstraint("status IN ('available', 'occupied', 'reserved')", name="check_status_valid"),
    )


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    table_id = Column(Integer, ForeignKey("tables.id", ondelete="CASCADE"), nullable=False)
    dish_id = Column(Integer, ForeignKey("dishes.id", ondelete="RESTRICT"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    total = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime, server_default=func.now())
    table = relationship("Table", back_populates="orders")
    dish = relationship("Dish", back_populates="orders")
    __table_args__ = (
        CheckConstraint("quantity > 0", name="check_quantity_positive"),
        CheckConstraint("status IN ('pending', 'served', 'paid', 'cancelled')", name="check_order_status_valid"),
    )