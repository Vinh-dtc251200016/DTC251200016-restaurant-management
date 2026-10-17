"""
Main: Khởi động FastAPI, khai báo API endpoints.
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import get_db, engine, Base

# Tự động tạo bảng nếu chưa có (không xóa dữ liệu cũ)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Restaurant Management API",
    description="API quản lý nhà hàng — món ăn, bàn, đơn hàng",
    version="1.0.0",
)

# CORS — cho phép frontend gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============ HEALTH ============
@app.get("/health", tags=["Health"])
def health_check():
    """Endpoint cho Docker healthcheck."""
    return {"status": "ok"}


# ============ DISHES ============
@app.get("/api/dishes", response_model=List[schemas.DishResponse], tags=["Dishes"])
def list_dishes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_dishes(db, skip=skip, limit=limit)


@app.get("/api/dishes/{dish_id}", response_model=schemas.DishResponse, tags=["Dishes"])
def get_dish(dish_id: int, db: Session = Depends(get_db)):
    dish = crud.get_dish(db, dish_id)
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    return dish


@app.post("/api/dishes", response_model=schemas.DishResponse, status_code=201, tags=["Dishes"])
def create_dish(dish: schemas.DishCreate, db: Session = Depends(get_db)):
    return crud.create_dish(db, dish)


@app.put("/api/dishes/{dish_id}", response_model=schemas.DishResponse, tags=["Dishes"])
def update_dish(dish_id: int, dish: schemas.DishUpdate, db: Session = Depends(get_db)):
    updated = crud.update_dish(db, dish_id, dish)
    if not updated:
        raise HTTPException(status_code=404, detail="Dish not found")
    return updated


@app.delete("/api/dishes/{dish_id}", status_code=204, tags=["Dishes"])
def delete_dish(dish_id: int, db: Session = Depends(get_db)):
    if not crud.delete_dish(db, dish_id):
        raise HTTPException(status_code=404, detail="Dish not found")
    return None


# ============ TABLES ============
@app.get("/api/tables", response_model=List[schemas.TableResponse], tags=["Tables"])
def list_tables(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_tables(db, skip=skip, limit=limit)


@app.get("/api/tables/{table_id}", response_model=schemas.TableResponse, tags=["Tables"])
def get_table(table_id: int, db: Session = Depends(get_db)):
    table = crud.get_table(db, table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    return table


@app.post("/api/tables", response_model=schemas.TableResponse, status_code=201, tags=["Tables"])
def create_table(table: schemas.TableCreate, db: Session = Depends(get_db)):
    existing = crud.get_table_by_number(db, table.table_number)
    if existing:
        raise HTTPException(status_code=400, detail="Table number already exists")
    return crud.create_table(db, table)


@app.put("/api/tables/{table_id}", response_model=schemas.TableResponse, tags=["Tables"])
def update_table(table_id: int, table: schemas.TableUpdate, db: Session = Depends(get_db)):
    updated = crud.update_table(db, table_id, table)
    if not updated:
        raise HTTPException(status_code=404, detail="Table not found")
    return updated


@app.delete("/api/tables/{table_id}", status_code=204, tags=["Tables"])
def delete_table(table_id: int, db: Session = Depends(get_db)):
    if not crud.delete_table(db, table_id):
        raise HTTPException(status_code=404, detail="Table not found")
    return None


# ============ ORDERS ============
@app.get("/api/orders", response_model=List[schemas.OrderResponse], tags=["Orders"])
def list_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_orders(db, skip=skip, limit=limit)


@app.get("/api/orders/{order_id}", response_model=schemas.OrderResponse, tags=["Orders"])
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.post("/api/orders", response_model=schemas.OrderResponse, status_code=201, tags=["Orders"])
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_order(db, order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/api/orders/{order_id}", response_model=schemas.OrderResponse, tags=["Orders"])
def update_order(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db)):
    updated = crud.update_order(db, order_id, order)
    if not updated:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated


@app.delete("/api/orders/{order_id}", status_code=204, tags=["Orders"])
def delete_order(order_id: int, db: Session = Depends(get_db)):
    if not crud.delete_order(db, order_id):
        raise HTTPException(status_code=404, detail="Order not found")
    return None