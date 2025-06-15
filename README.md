# Ứng dụng Quản lý Hoạt động Đoàn Hội

## 🚀 Giới thiệu

Dự án **"Xây dựng Hệ thống Quản lý các Hoạt động Đoàn Hội"** là một giải pháp phần mềm được phát triển để hỗ trợ các tổ chức Thiếu Nhi Thánh Thể cấp giáo xứ trong việc quản lý thành viên, lên kế hoạch và tổ chức sự kiện, điểm danh, và theo dõi quá trình hoạt động một cách hiệu quả. Hệ thống được thiết kế với giao diện thân thiện, dễ sử dụng, tích hợp các tính năng quan trọng để đáp ứng nhu cầu quản lý đa dạng.

## ✨ Tính năng nổi bật

* **Quản lý thành viên:** Cập nhật thông tin thành viên (Thiếu Nhi, Phụ Huynh, Nhân Sự, Trợ Tá) và phân công vai trò.
* **Quản lý phân đoàn:** Tạo và quản lý các phân đoàn, nhóm hoạt động.
* **Quản lý điểm danh:** Hỗ trợ điểm danh các buổi sinh hoạt, sự kiện thông qua QR Code.
* **Quản lý hoạt động:** Lập kế hoạch, theo dõi và đánh giá các hoạt động, sự kiện.
* **Import dữ liệu:** Dễ dàng nhập dữ liệu từ các nguồn khác (ví dụ: Google Sheets).
* **Trực quan hóa dữ liệu:** Biểu đồ, báo cáo giúp dễ dàng nắm bắt tình hình hoạt động.
* **Phân quyền người dùng:** Đảm bảo an toàn và bảo mật thông tin.

## 🛠️ Công nghệ sử dụng

* **Backend:** Flask (Python)
* **Frontend:** (Thông tin giao diện người dùng - cần bổ sung nếu có)
* **Cơ sở dữ liệu:** MySQL (hoặc các CSDL liên quan đến `XuDoan.sql`)
* **Công cụ:** PlantUML (cho biểu đồ kiến trúc và trình tự)

## ⚙️ Hướng dẫn cài đặt & Chạy dự án

1.  **Clone repository:**
    ```bash
    git clone <URL_repository_của_bạn>
    cd <tên_thư_mục_dự_án>
    ```

2.  **Cài đặt môi trường ảo (khuyến nghị):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Trên Linux/macOS
    # venv\Scripts\activate   # Trên Windows
    ```

3.  **Cài đặt các thư viện cần thiết:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Thiết lập cơ sở dữ liệu:**
    * Đảm bảo bạn đã cài đặt MySQL Server.
    * Tạo cơ sở dữ liệu mới (ví dụ: `XuDoan`).
    * Chạy script `database/XuDoan.sql` để tạo các bảng:
        ```bash
        mysql -u <username> -p <tên_csdl_của_bạn> < database/XuDoan.sql
        ```
    * Cập nhật thông tin kết nối cơ sở dữ liệu trong file cấu hình của ứng dụng (ví dụ: `config.py` hoặc `.env`).

5.  **Chạy ứng dụng:**
    ```bash
    python run.py  # Hoặc file chạy chính của ứng dụng Flask
    ```
    Ứng dụng sẽ chạy trên `http://127.0.0.1:5000` (hoặc cổng được cấu hình).

## 💡 Hướng phát triển trong tương lai

* **Hoàn thiện chức năng QR:** Tối ưu hóa việc tạo và quét QR Code cho điểm danh và các tác vụ khác.
* **Hoàn thiện chức năng import dữ liệu:** Hỗ trợ nhiều định dạng và nguồn dữ liệu hơn.
* **Hoàn thiện chức năng trực quan hóa dữ liệu:** Phát triển thêm các biểu đồ và báo cáo chi tiết.
* **Phát triển các mô hình so sánh và dự đoán:** Phân tích dữ liệu để đưa ra cái nhìn sâu sắc và dự báo.
* **Cập nhật dữ liệu vào Google Sheets:** Tích hợp đồng bộ hóa dữ liệu hai chiều.

## 📧 Liên hệ

Nếu có bất kỳ câu hỏi nào, vui lòng liên hệ:

* **Email:** [phuong.vht.0504@gmail.com](mailto:phuong.vht.0504@gmail.com)

Thông tin sinh viên, giảng viên:

**Võ Huỳnh Thanh Phương**
* **Mã số sinh viên:** 2151013072
* **Giảng viên hướng dẫn:** TS. LÊ VIẾT TUẤN
* **Trường:** Đại học Mở Thành phố Hồ Chí Minh
