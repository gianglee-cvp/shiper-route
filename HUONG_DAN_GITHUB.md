# Hướng dẫn đưa code lên GitHub

Vì ứng dụng này bao gồm cả **Python Backend** và **Web Frontend**, nên **GitHub Pages** không thể chạy được (GitHub Pages chỉ hỗ trợ web tĩnh).
Tuy nhiên, bạn có thể đưa toàn bộ mã nguồn lên GitHub để lưu trữ hoặc chia sẻ.

## Các bước thực hiện:

### 1. Tạo Repository trên GitHub
1. Đăng nhập vào [GitHub.com](https://github.com).
2. Bấm dấu **+** ở góc trên cùng bên phải -> chọn **New repository**.
3. Đặt tên repositories (ví dụ: `shiper-router-hanoi`).
4. Để chế độ **Public** hoặc **Private** tùy bạn.
5. **Không** tích chọn "Add a README file" (vì máy bạn đã có code rồi).
6. Bấm **Create repository**.

### 2. Đẩy code từ máy lên GitHub
Sau khi tạo xong, GitHub sẽ hiện ra các dòng lệnh. Bạn hãy copy dòng lệnh giống như dưới đây (thay `YOUR_USERNAME` bằng tên bạn):

Mở **Terminal** tại thư mục dự án (`d:\Project\shiper`) và chạy lần lượt:

```bash
git remote add origin https://github.com/YOUR_USERNAME/shiper-router-hanoi.git
git branch -M master
git push -u origin master
```

### 3. Demo cho người khác xem
Vì không deploy chạy trực tiếp trên web được, bạn có thể:
- **Cách 1**: Quay video màn hình lúc đang chạy demo trên máy local.
- **Cách 2**: Mang laptop đi demo và chạy 2 lệnh như trong file `HUONG_DAN_CHAY.md`.
- **Cách 3 (Nâng cao)**: Nếu muốn online thực sự, bạn cần thuê VPS hoặc dùng dịch vụ như **Render.com** (miễn phí) để host Backend Python.
