# Hướng dẫn chạy Demo Shipper Router

## 1. Chuẩn bị
Mở 2 cửa sổ CMD hoặc Terminal (hoặc 2 tab trong VS Code).
Đảm bảo bạn đang ở thư mục gốc của dự án: `d:\Project\shiper`

## 2. Chạy Backend (Server Python)
Đây là server chạy thuật toán tìm đường và xử lý bản đồ.
Ở terminal thứ 1, chạy lệnh:

```cmd
python backend/app.py
```

*Đợi khoảng 10-15 giây để load bản đồ cho đến khi thấy dòng:* 
`* Running on http://127.0.0.1:5000`

## 3. Chạy Frontend (Web Server)
Đây là server hiển thị giao diện bản đồ cho người dùng.
Ở terminal thứ 2, chạy lệnh:

```cmd
cd frontend
python -m http.server 8000
```

*Bạn sẽ thấy dòng:* `Serving HTTP on :: port 8000`

## 4. Truy cập & Demo
Mở trình duyệt (Chrome/Edge) và vào địa chỉ:
**http://localhost:8000**

### Kịch bản Demo:
1.  **Chọn điểm đi**: Bấm nút "Chọn trên bản đồ" (ô đầu tiên), sau đó click một điểm bất kỳ trên đường phố Hà Nội.
    *   *Lưu ý*: Bạn sẽ thấy một chấm xám (điểm click) và một chấm xanh (nút giao thông gần nhất được server chọn).
2.  **Chọn điểm đến**: Bấm nút "Chọn trên bản đồ" (ô thứ 2), click một điểm khác.
3.  **Tìm đường**: Bấm nút "Tìm đường tối ưu".
    *   Hệ thống sẽ vẽ đường đi chính xác theo men đường giao thông.
4.  **Thử thuật toán khác**: Đổi từ "Dijkstra" sang "A*" và bấm tìm lại để so sánh (nếu đường dài sẽ thấy tốc độ xử lý khác nhau).
