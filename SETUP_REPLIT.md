# 🎮 Setup Dodger Pro Max trên Replit

Hướng dẫn chi tiết để chơi game trực tiếp trên web bằng Replit!

## ✨ Cách Nhanh Nhất (1 phút)

1. **Truy cập**: https://replit.com/github/YourUsername/Dodger-main
   - Thay `YourUsername` bằng username GitHub của bạn
2. **Click "Import from GitHub"**
3. **Click "Run"** → Game sẽ chạy ngay!

## 📝 Hướng Dẫn Chi Tiết

### Bước 1: Chuẩn Bị Repository GitHub
Đảm bảo phải có những file này trong repo:
```
Dodger-main/
├── dodger.py          ← File chính (chứa def main)
├── constants.py       ← File hằng số
├── maps.py            ← Cấu hình bản đồ
├── menus.py           ← Giao diện menu
├── question.py        ← Hệ thống câu hỏi Python
├── items.py           ← Hệ thống xu & powerup
├── enemies.py         ← AI quái vật
├── requirements.txt   ← Dependencies (pygame==2.6.1)
└── xu.png             ← Hình ảnh xu
```

### Bước 2: Tạo `requirements.txt`
Tạo file `requirements.txt` trong thư mục gốc:
```
pygame==2.6.1
numpy==1.24.0
```

### Bước 3: Tạo `.replit`
Để Replit biết cách chạy game, tạo file `.replit` (không có tên):
```bash
language = "python3"
run = "python dodger.py"
entrypoint = "dodger.py"
```

### Bước 4: Commit & Push lên GitHub
```bash
git add .
git commit -m "Add Replit support"
git push origin main
```

### Bước 5: Import vào Replit
1. Truy cập https://replit.com (đăng nhập nếu cần)
2. Click "+" hoặc "Create Repl"
3. Chọn "Import from GitHub"
4. Dán link repo GitHub:
   ```
   https://github.com/YourUsername/Dodger-main
   ```
5. Click "Import"
6. Chờ Replit cài đặt (2-3 phút)
7. Click nút **Run** (tam giác xanh)

## 🎮 Chơi Game
Sau khi click Run, game sẽ khởi động với giao diện pygame.
- Ấn phím **← →** để di chuyển
- Ấn **SPACE** để nhảy
- Chơi như bình thường!

## 🔗 Chia Sẻ Link
Sau khi setup xong, Replit sẽ tạo URL riêng:
```
https://Dodger-main.username.repl.co
```

**Chia sẻ link này với bạn bè!** Họ có thể click vào chơi ngay mà không cần cài gì.

## 🐛 Xử Lý Lỗi

### Lỗi: "ModuleNotFoundError: No module named 'pygame'"
**Giải pháp**: Thêm `pygame==2.6.1` vào `requirements.txt` làm tệp tiện ích.

### Lỗi: "pygame.display" không hiển thị
**Giải pháp**: Replit sử dụng giao diện webGL. Pygame sẽ tự render trong browser.

### Game chạy nhưng không có hình ảnh
**Giải pháp**: Đảm bảo `xu.png` và các sprite files ở đúng thư mục.

## 📱 Thay Đổi Kích Thước Màn Hình (Tùy Chọn)

Nếu game quá to/nhỏ khi chơi trên Replit, chỉnh trong `constants.py`:
```python
WIDTH = 800   # Giảm từ 1000
HEIGHT = 600  # Giữ nguyên hoặc giảm
```

## 🌟 Mẹo Khác

1. **Lưu trữ trực tuyến**: Đính kèm tất cả ảnh vào repo
2. **Cải thiện tốc độ**: Dùng ảnh nhỏ hơn (.png compressed)
3. **Chia sẻ dễ**: Copy URL từ Replit, gửi cho bạn bè
4. **Không phải login**: Bạn bè không cần tài khoản Replit để chơi!

## ✅ Xác Nhận Hoàn Tất

Game đã sẵn sàng chơi trực tiếp! 🎉

Nếu có vấn đề, kiểm tra:
- [ ] Tất cả file `.py` đã được push
- [ ] `requirements.txt` có pygame
- [ ] `.replit` file tồn tại
- [ ] Hình ảnh (xu.png) ở đúng thư mục

---

**Thêm link vào GitHub Pages (index.html)**:

Thêm button ở `index.html`:
```html
<a href="https://replit.com/github/YourUsername/Dodger-main" class="play-button">
    ▶️ CHƠI NGAY TRÊN WEB
</a>
```

Giờ mọi người có thể chơi game trực tiếp từ trang web! 🚀
