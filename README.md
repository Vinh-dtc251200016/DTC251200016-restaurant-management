# Hệ thống Quản lý Nhà hàng / Order

**Sinh viên thực hiện:** Nguyễn Công Vĩnh  
**Mã số sinh viên:** DTC251200016  
**Đề tài:** Đề 12 - Hệ thống Quản lý Nhà hàng / Order

---

## 📖 Giới thiệu dự án
Dự án xây dựng một hệ thống website quản lý nhà hàng cho phép quản lý món ăn, bàn ăn và đơn hàng. Hệ thống được triển khai hoàn chỉnh trên môi trường Docker Compose, tích hợp các công cụ giám sát (Monitoring) và quản lý log tập trung (Logging) theo tiêu chuẩn DevOps.

## 🛠 Tech Stack
- **Backend:** Python (FastAPI), SQLAlchemy
- **Frontend:** HTML, CSS, JavaScript (Vanilla)
- **Database:** PostgreSQL 15
- **DB Tool:** pgAdmin 4
- **Web Server:** Nginx (Reverse Proxy, HTTPS, Security Headers)
- **Monitoring:** Prometheus, Grafana, Node Exporter, cAdvisor
- **Logging:** Loki, Promtail (LogQL)
- **Containerization:** Docker, Docker Compose
- **Version Control:** GitHub

## 📂 Cấu trúc thư mục
```text
restaurant-management/
├── backend/              # Source code FastAPI
│   ├── app/              # Models, Schemas, CRUD, Main
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/             # Giao diện HTML/CSS/JS
│   ├── index.html
│   ├── style.css
│   ├── app.js
│   └── Dockerfile
├── db/                   # Script khởi tạo Database
│   └── init.sql
├── nginx/                # Cấu hình Nginx & SSL Cert
│   ├── nginx.conf
│   └── certs/
├── monitoring/           # Cấu hình Prometheus
│   └── prometheus/
├── logging/              # Cấu hình Loki & Promtail
│   ├── loki/
│   └── promtail/
├── docker-compose.yml    # File điều phối 11 services
├── .env                  # Biến môi trường (không push lên Git)
└── README.md