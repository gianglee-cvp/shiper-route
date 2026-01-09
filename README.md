# Hanoi Shipper Router App

Ứng dụng tìm đường tối ưu cho shipper tại khu vực Hà Nội bằng thuật toán Dijkstra và A*.

## 🛠 Yêu cầu hệ thống
- **Python 3.8+**
- Trình duyệt web hiện đại (Chrome, Edge, Firefox,...)

## 🚀 Hướng dẫn cài đặt và chạy

### 1. Chuẩn bị Backend (Python)
Mở terminal tại thư mục gốc của dự án (`shiper/`):

```bash
# Di chuyển vào thư mục backend
cd backend

# Tạo môi trường ảo (Khuyến khích)
python -m venv venv

# Kích hoạt môi trường ảo:
# Trên Windows:
.\venv\Scripts\activate
# Trên Mac/Linux:
source venv/bin/activate

# Cài đặt các thư viện cần thiết
pip install -r requirements.txt

# Chạy server
python app.py
```
*Ghi chú: Lần đầu chạy có thể mất vài phút để tải dữ liệu bản đồ Hà Nội.*

### 2. Chạy Frontend (Web)
- Mở thư mục `frontend/`.
- Click đúp vào file `index.html` để mở trên trình duyệt.
- Bạn cũng có thể dùng extension "Live Server" trên VS Code để chạy.

## 📖 Cách sử dụng
1. Bấm nút **"Chọn trên bản đồ"** tại mục "Điểm bắt đầu".
2. Click vào một vị trí trên bản đồ Hanoi.
3. Làm tương tự cho **"Điểm đến"**.
4. Chọn thuật toán (**Dijkstra** hoặc **A***).
5. Bấm **"Tìm đường tối ưu"** và chờ kết quả hiển thị.

## 📂 Cấu trúc dự án
- `/backend`: Chứa server Flask và logic thuật toán đồ thị.
- `/frontend`: Giao diện người dùng (Bản đồ Leaflet, CSS, JS).
- `hanoi_graph.graphml`: Dữ liệu bản đồ đã được đóng gói.
