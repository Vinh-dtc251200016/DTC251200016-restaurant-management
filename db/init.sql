-- ============================================
-- Database: restaurant
-- Mô tả: Khởi tạo schema cho hệ thống quản lý nhà hàng
-- ============================================

-- Bảng 1: Món ăn
CREATE TABLE IF NOT EXISTS dishes (
    id           SERIAL PRIMARY KEY,
    name         VARCHAR(100) NOT NULL,
    description  TEXT,
    price        NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
    category     VARCHAR(50),
    is_available BOOLEAN DEFAULT TRUE,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng 2: Bàn ăn
CREATE TABLE IF NOT EXISTS tables (
    id           SERIAL PRIMARY KEY,
    table_number VARCHAR(10) NOT NULL UNIQUE,
    capacity     INT DEFAULT 4 CHECK (capacity > 0),
    status       VARCHAR(20) DEFAULT 'available'
                 CHECK (status IN ('available', 'occupied', 'reserved')),
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng 3: Đơn hàng
CREATE TABLE IF NOT EXISTS orders (
    id         SERIAL PRIMARY KEY,
    table_id   INT NOT NULL REFERENCES tables(id) ON DELETE CASCADE,
    dish_id    INT NOT NULL REFERENCES dishes(id) ON DELETE RESTRICT,
    quantity   INT NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10, 2) NOT NULL,
    total      NUMERIC(10, 2) NOT NULL,
    status     VARCHAR(20) DEFAULT 'pending'
               CHECK (status IN ('pending', 'served', 'paid', 'cancelled')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index để truy vấn nhanh hơn
CREATE INDEX IF NOT EXISTS idx_orders_table    ON orders(table_id);
CREATE INDEX IF NOT EXISTS idx_orders_status   ON orders(status);
CREATE INDEX IF NOT EXISTS idx_dishes_category ON dishes(category);

-- Dữ liệu mẫu để test
INSERT INTO dishes (name, description, price, category) VALUES
    ('Phở bò',     'Phở bò truyền thống Hà Nội', 50000, 'Món nước'),
    ('Cơm tấm',    'Cơm tấm sườn bì chả',        45000, 'Món khô'),
    ('Bún chả',    'Bún chả Hà Nội',             40000, 'Món nước'),
    ('Gỏi cuốn',   'Gỏi cuốn tôm thịt',          30000, 'Khai vị'),
    ('Trà đá',     'Trà đá miễn phí',            0,     'Đồ uống'),
    ('Cà phê sữa', 'Cà phê sữa đá',              25000, 'Đồ uống')
ON CONFLICT DO NOTHING;

INSERT INTO tables (table_number, capacity, status) VALUES
    ('B01', 2, 'available'),
    ('B02', 4, 'available'),
    ('B03', 4, 'available'),
    ('B04', 6, 'available'),
    ('B05', 8, 'available')
ON CONFLICT DO NOTHING;