
## 1. Thông tin cá nhân
- **Họ và Tên**: Nguyễn Phạm Chí Bảo
- **Mã Sinh Viên**: 22678881
- **Lớp**: DHKHDL18A
-**STT**: 04

---

## 2. Giới thiệu Project
### 🔹 Mô tả
Ứng dụng quản lý công việc (To-Do List) giúp người dùng tạo, quản lý và theo dõi tiến độ công việc cá nhân. Các tính năng chính bao gồm:
- **Đăng ký & Đăng nhập**: Người dùng có thể tạo tài khoản và đăng nhập vào hệ thống.
- **Quản lý công việc**: Thêm, sửa, xóa công việc, cập nhật trạng thái hoàn thành.
- **Hình đại diện**: Có thể cập nhật hình đại diện của mình 
- **Thông báo công việc trễ hạn**: Hiển thị số lượng công việc quá hạn ngay trên avatar.
- **Hỗ trợ ảnh đính kèm**: Mỗi công việc có thể kèm theo một hình ảnh minh họa.
- **Giao diện Single Column**: Hiển thị danh sách công việc theo dạng một cột dọc.

### 🛠 Công nghệ sử dụng
- **Backend**: Flask, Flask-Login, SQLAlchemy
- **Frontend**: HTML, CSS, Bootstrap
- **Database**: SQLite 

---

## 3. Hướng dẫn Cài đặt
### 🔹 Bước 1: Clone Repository
```sh
git clone git clone https://github.com/yourusername/ptud-gk-de-2.git
cd ptud-gk-de-2

```

### 🔹 Bước 2: Tạo Virtual Environment & Cài Đặt Dependencies
```sh
python -m venv venv
source venv/bin/activate  # Trên macOS/Linux
venv\Scripts\activate    # Trên Windows
pip install -r requirements.txt
```

### 🔹 Bước 3: Chạy Ứng Dụng
```sh
flask run
```

Ứng dụng sẽ chạy tại: `http://127.0.0.1:5000/`



