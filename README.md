# RAG Basics - Qdrant Tutorial

Đây là mã nguồn mẫu cho bài hướng dẫn sử dụng Qdrant vector database, top-k, và metadata filtering (pre-filtering) trong hệ thống RAG (Retrieval-Augmented Generation).

## Hướng dẫn sử dụng

1. **Khởi động Qdrant server:**
   ```bash
   docker compose up -d
   ```

2. **Tạo môi trường ảo (khuyên dùng) và cài đặt thư viện:**
   - **Linux/macOS:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     pip install -r requirements.txt
     ```
   - **Windows:**
     ```cmd
     python -m venv venv
     venv\Scripts\activate
     pip install -r requirements.txt
     ```

3. **Chạy ứng dụng API:**
   ```bash
   python main.py
   ```

4. **Truy cập Swagger UI:**
   Mở trình duyệt và truy cập `http://localhost:1810/docs` để gửi các truy vấn tìm kiếm bằng REST API.

## Cấu trúc mã nguồn

- `docker-compose.yml`: Cấu hình Docker để khởi chạy Qdrant server.
- `main.py`: File mã nguồn chính, khởi tạo Database, sinh embedding, insert dữ liệu, lập chỉ mục (Payload Index), và tạo API Search bằng FastAPI.
- `requirements.txt`: Các thư viện phụ thuộc có ghim phiên bản chuẩn để tránh lỗi tương thích.
- `sample_data.json`: Dữ liệu mẫu (nếu bạn muốn import từ file thay vì lấy thẳng từ python list).
