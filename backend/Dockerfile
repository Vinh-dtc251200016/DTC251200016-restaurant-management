# ============================================
# Stage 1: Builder - cài dependencies
# ============================================
FROM python:3.11-slim AS builder

WORKDIR /app

# Cài build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements trước để cache layer
COPY requirements.txt .

# Cài vào thư mục riêng (để copy sang stage 2)
RUN pip install --no-cache-dir --user -r requirements.txt


# ============================================
# Stage 2: Runtime - image cuối cùng
# ============================================
FROM python:3.11-slim

# Tạo user non-root (hardening)
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Copy dependencies từ builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy code
COPY --chown=appuser:appuser app/ ./app/

# Chuyển sang user non-root
USER appuser

# Thêm local bin vào PATH
ENV PATH=/home/appuser/.local/bin:$PATH

# Expose port
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Chạy uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]