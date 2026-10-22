# Test cases – Tuần 5 – Chức năng Đăng nhập

## 1. Thông tin chung

| Mục | Nội dung |
|---|---|
| Ứng dụng | Swag Labs (Android) |
| Package / Activity | `com.swaglabsmobileapp` / `.MainActivity` |
| Màn hình kiểm thử | Login |
| Công cụ | Appium 2 + UiAutomator2, Python + pytest |
| Thiết bị | Android emulator (`emulator-5554`) |
| Tài khoản hợp lệ | `standard_user` / `secret_sauce` |
| Tài khoản bị khoá | `locked_out_user` / `secret_sauce` |
| Người viết | Nhóm App |
| Ngày viết | 22/10/2026 |
| Phạm vi | 3 test case cho chức năng Đăng nhập |

**Ngoài phạm vi tuần 5:** đăng ký tài khoản, quên mật khẩu, đổi mật khẩu, đăng nhập bằng mạng xã hội.

## 2. Điều kiện chung

- App Swag Labs đã được cài trên máy ảo Android.
- Appium server đang chạy tại `http://127.0.0.1:4723`.
- Driver `uiautomator2` đã được cài.
- Trước mỗi test case, app được khởi động lại từ trạng thái sạch (chưa đăng nhập).
- Các phần tử được xác định bằng **accessibility id** có sẵn trong app:
  - Ô tên đăng nhập: `test-Username`
  - Ô mật khẩu: `test-Password`
  - Nút đăng nhập: `test-LOGIN`
  - Màn hình sản phẩm: `test-PRODUCTS`
  - Khung thông báo lỗi: `test-Error message`

## 3. Danh sách test case

| ID | Tên test case | Ưu tiên | Kết quả mong đợi tóm tắt |
|---|---|---|---|
| TC-LOGIN-01 | Đăng nhập thành công với tài khoản hợp lệ | Cao | Vào được màn hình PRODUCTS |
| TC-LOGIN-02 | Đăng nhập với tài khoản bị khoá | Cao | Hiện thông báo tài khoản bị khoá |
| TC-LOGIN-03 | Đăng nhập khi bỏ trống mật khẩu | Trung bình | Hiện thông báo `Password is required` |

## 4. Chi tiết từng test case

### TC-LOGIN-01 – Đăng nhập thành công với tài khoản hợp lệ

**Mục tiêu:** Kiểm tra người dùng nhập đúng tên đăng nhập và mật khẩu thì vào được màn hình danh sách sản phẩm.

**Tiền điều kiện:**
- App đang ở màn hình Login.
- Chưa có phiên đăng nhập nào trước đó.

**Dữ liệu kiểm thử:**

| Trường | Giá trị |
|---|---|
| Username | `standard_user` |
| Password | `secret_sauce` |

**Các bước thực hiện:**

1. Khởi động app Swag Labs.
2. Chờ màn hình Login hiển thị (ô `test-Username` xuất hiện).
3. Nhập `standard_user` vào ô Username.
4. Nhập `secret_sauce` vào ô Password.
5. Bấm nút `LOGIN`.
6. Chờ tối đa 60 giây để màn hình PRODUCTS hiển thị.

**Kết quả mong đợi:**
- App chuyển sang màn hình PRODUCTS.
- Tiêu đề `PRODUCTS` hiển thị.
- Danh sách sản phẩm hiển thị.
- Không có thông báo lỗi.
- Nút LOGIN không còn hiển thị.

**Kịch bản tự động:** `test_dang_nhap_dung_vao_duoc_manh_products`

---

### TC-LOGIN-02 – Đăng nhập với tài khoản bị khoá

**Mục tiêu:** Kiểm tra app từ chối tài khoản đang bị khoá và hiển thị đúng thông báo.

**Tiền điều kiện:**
- App đang ở màn hình Login.
- Chưa có phiên đăng nhập nào trước đó.

**Dữ liệu kiểm thử:**

| Trường | Giá trị |
|---|---|
| Username | `locked_out_user` |
| Password | `secret_sauce` |

**Các bước thực hiện:**

1. Khởi động app Swag Labs.
2. Chờ màn hình Login hiển thị.
3. Nhập `locked_out_user` vào ô Username.
4. Nhập `secret_sauce` vào ô Password.
5. Bấm nút `LOGIN`.
6. Chờ khung thông báo lỗi hiển thị.

**Kết quả mong đợi:**
- App vẫn ở màn hình Login, không vào được PRODUCTS.
- Khung thông báo lỗi màu đỏ hiển thị.
- Nội dung thông báo: `Sorry, this user has been locked out.`
- Tên đăng nhập và mật khẩu vẫn còn trong hai ô nhập.

**Kịch bản tự động:** `test_dang_nhap_tai_khoan_bi_khoa`

---

### TC-LOGIN-03 – Đăng nhập khi bỏ trống mật khẩu

**Mục tiêu:** Kiểm tra app bắt buộc nhập mật khẩu trước khi đăng nhập.

**Tiền điều kiện:**
- App đang ở màn hình Login.
- Ô mật khẩu đang trống.
- Chưa có phiên đăng nhập nào trước đó.

**Dữ liệu kiểm thử:**

| Trường | Giá trị |
|---|---|
| Username | `standard_user` |
| Password | *(để trống)* |

**Các bước thực hiện:**

1. Khởi động app Swag Labs.
2. Chờ màn hình Login hiển thị.
3. Nhập `standard_user` vào ô Username.
4. Không nhập gì vào ô Password (đảm bảo ô này đang trống).
5. Bấm nút `LOGIN`.
6. Chờ khung thông báo lỗi hiển thị.

**Kết quả mong đợi:**
- App vẫn ở màn hình Login, không vào được PRODUCTS.
- Khung thông báo lỗi màu đỏ hiển thị.
- Nội dung thông báo: `Password is required`
- Ô Username vẫn giữ giá trị `standard_user`.

**Kịch bản tự động:** `test_dang_nhap_bi_trong_mat_khau`

## 5. Cách chạy bộ kiểm thử

Từ thư mục gốc của repo:

```powershell
# Kích hoạt môi trường ảo
.\.venv\Scripts\Activate.ps1

# Chạy cả 3 test case
pytest tuan-05/test_login.py -v
```

Kết quả mong đợi:

```text
3 passed
```

## 6. Ghi chú kiểm chứng

- Bộ test đã được chạy trên emulator `Pixel_7` (`emulator-5554`) ngày 22/10/2026.
- Kết quả: **3/3 PASSED**.
- Thời gian chạy: khoảng 46 giây.
- Ảnh minh chứng nằm trong `tuan-05/anh/`:
  - `01_dang_nhap_dung_vao_manh_PRODUCTS.png`
  - `02_tai_khoan_bi_khoa.png`
  - `03_bo_trong_mat_khau.png`
