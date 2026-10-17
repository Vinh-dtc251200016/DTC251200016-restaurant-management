"""
CRUD: Các hàm xử lý database cho dishes, tables, orders.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app import models, schemas


# ============ DISH ============
def get_dishes(db: Session, skip: int = 0, limit: int = 100) -> List[models.Dish]:
    """Lấy danh sách món ăn (có phân trang)."""
    return db.query(models.Dish).offset(skip).limit(limit).all()


def get_dish(db: Session, dish_id: int) -> Optional[models.Dish]:
    """Lấy 1 món ăn theo id."""
    return db.query(models.Dish).filter(models.Dish.id == dish_id).first()


def create_dish(db: Session, dish: schemas.DishCreate) -> models.Dish:
    """Tạo món ăn mới."""
    db_dish = models.Dish(**dish.model_dump())
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    return db_dish


def update_dish(db: Session, dish_id: int, dish: schemas.DishUpdate) -> Optional[models.Dish]:
    """Cập nhật món ăn."""
    db_dish = get_dish(db, dish_id)
    if not db_dish:
        return None
    # Chỉ update các trường được gửi lên (exclude_unset=True)
    update_data = dish.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_dish, key, value)
    db.commit()
    db.refresh(db_dish)
    return db_dish


def delete_dish(db: Session, dish_id: int) -> bool:
    """Xóa món ăn."""
    db_dish = get_dish(db, dish_id)
    if not db_dish:
        return False
    db.delete(db_dish)
    db.commit()
    return True


# ============ TABLE ============
def get_tables(db: Session, skip: int = 0, limit: int = 100) -> List[models.Table]:
    return db.query(models.Table).offset(skip).limit(limit).all()


def get_table(db: Session, table_id: int) -> Optional[models.Table]:
    return db.query(models.Table).filter(models.Table.id == table_id).first()


def get_table_by_number(db: Session, table_number: str) -> Optional[models.Table]:
    return db.query(models.Table).filter(models.Table.table_number == table_number).first()


def create_table(db: Session, table: schemas.TableCreate) -> models.Table:
    db_table = models.Table(**table.model_dump())
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table


def update_table(db: Session, table_id: int, table: schemas.TableUpdate) -> Optional[models.Table]:
    db_table = get_table(db, table_id)
    if not db_table:
        return None
    update_data = table.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_table, key, value)
    db.commit()
    db.refresh(db_table)
    return db_table


def delete_table(db: Session, table_id: int) -> bool:
    db_table = get_table(db, table_id)
    if not db_table:
        return False
    db.delete(db_table)
    db.commit()
    return True


# ============ ORDER ============
def get_orders(db: Session, skip: int = 0, limit: int = 100) -> List[models.Order]:
    return db.query(models.Order).offset(skip).limit(limit).all()


def get_order(db: Session, order_id: int) -> Optional[models.Order]:
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def create_order(db: Session, order: schemas.OrderCreate) -> models.Order:
    """Tạo đơn hàng. Tự tính unit_price và total."""
    # Lấy giá món hiện tại
    dish = get_dish(db, order.dish_id)
    if not dish:
        raise ValueError(f"Dish with id {order.dish_id} not found")

    # Kiểm tra bàn tồn tại
    table = get_table(db, order.table_id)
    if not table:
        raise ValueError(f"Table with id {order.table_id} not found")

    # Tính total
    unit_price = dish.price
    total = unit_price * order.quantity

    db_order = models.Order(
        table_id=order.table_id,
        dish_id=order.dish_id,
        quantity=order.quantity,
        unit_price=unit_price,
        total=total,
        status="pending",
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def update_order(db: Session, order_id: int, order: schemas.OrderUpdate) -> Optional[models.Order]:
    db_order = get_order(db, order_id)
    if not db_order:
        return None
    update_data = order.model_dump(exclude_unset=True)
    # Nếu đổi quantity → tính lại total
    if "quantity" in update_data:
        db_order.total = db_order.unit_price * update_data["quantity"]
    for key, value in update_data.items():
        setattr(db_order, key, value)
    db.commit()
    db.refresh(db_order)
    return db_order


def delete_order(db: Session, order_id: int) -> bool:
    db_order = get_order(db, order_id)
    if not db_order:
        return False
    db.delete(db_order)
    db.commit()
    return True