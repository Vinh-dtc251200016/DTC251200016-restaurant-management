// ============================================
// Cấu hình API
// ============================================
const API_URL = "/api";
// ============================================
// TAB SWITCHING
// ============================================
document.querySelectorAll(".tab-btn").forEach(btn => {
    btn.addEventListener("click", () => {
        // Bỏ active tất cả
        document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
        document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));
        // Active cái được click
        btn.classList.add("active");
        document.getElementById(btn.dataset.tab).classList.add("active");
    });
});


// ============================================
// HÀM GỌI API CHUNG
// ============================================
async function apiCall(endpoint, method = "GET", body = null) {
    const options = {
        method: method,
        headers: { "Content-Type": "application/json" }
    };
    if (body) options.body = JSON.stringify(body);

    const response = await fetch(`${API_URL}${endpoint}`, options);
    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: "Lỗi không xác định" }));
        throw new Error(error.detail || `HTTP ${response.status}`);
    }
    // 204 No Content → không có body
    if (response.status === 204) return null;
    return response.json();
}


// ============================================
// ĐỊNH DẠNG
// ============================================
function formatPrice(price) {
    return Number(price).toLocaleString("vi-VN") + " đ";
}

function getStatusBadge(status) {
    const labels = {
        available: "Còn trống",
        occupied: "Đang dùng",
        reserved: "Đã đặt",
        pending: "Chờ xử lý",
        served: "Đã phục vụ",
        paid: "Đã thanh toán",
        cancelled: "Đã hủy"
    };
    return `<span class="badge badge-${status}">${labels[status] || status}</span>`;
}


// ============================================
// TAB MÓN ĂN
// ============================================
async function loadDishes() {
    try {
        const dishes = await apiCall("/dishes");
        const tbody = document.querySelector("#dishes-table tbody");
        tbody.innerHTML = "";

        dishes.forEach(d => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${d.id}</td>
                <td>${d.name}</td>
                <td>${formatPrice(d.price)}</td>
                <td>${d.category || "-"}</td>
                <td>${d.is_available ? "Còn bán" : "Ngừng bán"}</td>
                <td><button class="btn-delete" onclick="deleteDish(${d.id})">Xóa</button></td>
            `;
            tbody.appendChild(tr);
        });
    } catch (err) {
        console.error("Lỗi load dishes:", err);
        alert("Không tải được danh sách món ăn: " + err.message);
    }
}

async function deleteDish(id) {
    if (!confirm(`Xóa món ăn ID ${id}?`)) return;
    try {
        await apiCall(`/dishes/${id}`, "DELETE");
        loadDishes();
    } catch (err) {
        alert("Lỗi xóa: " + err.message);
    }
}

document.getElementById("dish-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = {
        name: document.getElementById("dish-name").value,
        description: document.getElementById("dish-description").value || null,
        price: parseFloat(document.getElementById("dish-price").value),
        category: document.getElementById("dish-category").value || null,
        is_available: true
    };
    try {
        await apiCall("/dishes", "POST", data);
        e.target.reset();
        loadDishes();
    } catch (err) {
        alert("Lỗi thêm món: " + err.message);
    }
});


// ============================================
// TAB BÀN ĂN
// ============================================
async function loadTables() {
    try {
        const tables = await apiCall("/tables");
        const tbody = document.querySelector("#tables-table tbody");
        tbody.innerHTML = "";

        tables.forEach(t => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${t.id}</td>
                <td>${t.table_number}</td>
                <td>${t.capacity}</td>
                <td>${getStatusBadge(t.status)}</td>
            `;
            tbody.appendChild(tr);
        });

        // Cập nhật dropdown trong form order
        const selectTable = document.getElementById("order-table");
        selectTable.innerHTML = '<option value="">-- Chọn bàn --</option>';
        tables.forEach(t => {
            selectTable.innerHTML += `<option value="${t.id}">${t.table_number} (${t.capacity} chỗ)</option>`;
        });
    } catch (err) {
        console.error("Lỗi load tables:", err);
    }
}

document.getElementById("table-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = {
        table_number: document.getElementById("table-number").value,
        capacity: parseInt(document.getElementById("table-capacity").value),
        status: "available"
    };
    try {
        await apiCall("/tables", "POST", data);
        e.target.reset();
        document.getElementById("table-capacity").value = 4;
        loadTables();
    } catch (err) {
        alert("Lỗi thêm bàn: " + err.message);
    }
});


// ============================================
// TAB ĐƠN HÀNG
// ============================================
async function loadOrders() {
    try {
        const orders = await apiCall("/orders");
        const tbody = document.querySelector("#orders-table tbody");
        tbody.innerHTML = "";

        orders.forEach(o => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${o.id}</td>
                <td>Bàn #${o.table_id}</td>
                <td>Món #${o.dish_id}</td>
                <td>${o.quantity}</td>
                <td>${formatPrice(o.unit_price)}</td>
                <td><strong>${formatPrice(o.total)}</strong></td>
                <td>${getStatusBadge(o.status)}</td>
            `;
            tbody.appendChild(tr);
        });
    } catch (err) {
        console.error("Lỗi load orders:", err);
    }
}

async function loadDishOptions() {
    try {
        const dishes = await apiCall("/dishes");
        const selectDish = document.getElementById("order-dish");
        selectDish.innerHTML = '<option value="">-- Chọn món --</option>';
        dishes.forEach(d => {
            selectDish.innerHTML += `<option value="${d.id}">${d.name} - ${formatPrice(d.price)}</option>`;
        });
    } catch (err) {
        console.error("Lỗi load dish options:", err);
    }
}

document.getElementById("order-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = {
        table_id: parseInt(document.getElementById("order-table").value),
        dish_id: parseInt(document.getElementById("order-dish").value),
        quantity: parseInt(document.getElementById("order-quantity").value)
    };
    try {
        await apiCall("/orders", "POST", data);
        e.target.reset();
        document.getElementById("order-quantity").value = 1;
        loadOrders();
    } catch (err) {
        alert("Lỗi tạo đơn: " + err.message);
    }
});


// ============================================
// KHỞI ĐỘNG
// ============================================
window.addEventListener("DOMContentLoaded", () => {
    loadDishes();
    loadTables();
    loadOrders();
    loadDishOptions();
    console.log("✅ Frontend đã load, API URL:", API_URL);
});