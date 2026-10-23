# KTPM – Nhóm App (Appium + Swag Labs)

Repo bài thực hành kiểm thử tự động trên ứng dụng **Swag Labs** (Android),
dùng **Appium + UiAutomator2**, viết bằng **Python + pytest**.

## Tiến độ

| Tuần | Nội dung | Trạng thái |
|---|---|---|
| 4 | Cài môi trường và chạy smoke test đầu tiên | Hoàn thành |
| 5 | 3 test case cho chức năng Đăng nhập | Hoàn thành, 3/3 PASSED |
| 6 | Slide trình bày vòng 1: kiểm thử tự động là gì, kiến trúc Appium và demo Đăng nhập | Hoàn thành bộ slide + ghi chú |

## 1. Thông tin ứng dụng

- Ứng dụng: **Swag Labs** (Android)
- Package: `com.swaglabsmobileapp`
- Activity: `.MainActivity`
- Tải `.apk` tại: <https://github.com/saucelabs/sample-app-mobile/releases>
- Tài khoản dùng để kiểm thử:

| Tài khoản | Mật khẩu | Mục đích |
|---|---|---|
| `standard_user` | `secret_sauce` | Đăng nhập thành công |
| `locked_out_user` | `secret_sauce` | Kiểm tra tài khoản bị khoá |
| `standard_user` | *(để trống)* | Kiểm tra bắt buộc nhập mật khẩu |

## 2. Cấu trúc kho mã

```text
.
├─ requirements.txt          # thư viện Python cần cài
├─ tuan-04/
│  ├─ test_smoke.py          # smoke test: mở app, kiểm tra ô đăng nhập
│  ├─ notes.md               # ghi chú tuần 4
│  └─ anh/                   # ảnh chụp màn hình chạy thành công
├─ tuan-05/
│  ├─ test_login.py          # 3 test case Đăng nhập
│  ├─ testcases.md           # mô tả 3 test case bằng lời
│  ├─ notes.md               # ghi chú tuần 5 (mỗi thành viên tự viết)
│  └─ anh/                   # ảnh kết quả chạy 3 test case
├─ tuan-06/
│  ├─ slides.pdf             # slide trình bày vòng 1 (8 trang)
│  ├─ slides.html            # bản nguồn để chỉnh sửa và xuất lại PDF
│  └─ notes.md               # ghi chú tuần 6: phần đọc, góp ý, việc cải thiện
└─ README.md
```

## 3. Cài đặt môi trường

### 3.1. Phần mềm bắt buộc

| Phần mềm | Phiên bản | Kiểm tra |
|---|---|---|
| Node.js | 18 trở lên | `node -v` |
| JDK | 17 | `java -version` |
| Android Studio | mới nhất | có `adb` trong `platform-tools` |
| Python | 3.10 trở lên | `python --version` |
| Appium | 2 trở lên | `appium --version` |

Thêm biến môi trường (Windows):

- `JAVA_HOME` → thư mục cài JDK 17
- `ANDROID_HOME` → `%LOCALAPPDATA%\Android\Sdk` (hoặc đường dẫn SDK thực tế)
- Thêm vào `PATH`: `%ANDROID_HOME%\platform-tools` và `%ANDROID_HOME%\emulator`

Mở terminal mới rồi kiểm tra:

```powershell
java -version
adb devices
```

### 3.2. Tạo máy ảo Android (AVD)

Android Studio → **Device Manager** → **Create Virtual Device** → chọn Pixel 5
(hoặc tương tự) → hệ điều hành **API 33+** → Finish → bấm ▶ để khởi động.

Máy yếu có thể dùng điện thoại Android thật: bật **USB debugging**, cắm cáp,
rồi dùng `adb devices` để lấy mã thiết bị.

> Nên dùng **Cold boot** khi máy ảo chạy chập chờn. Nếu emulator hay treo,
> thử chạy với GPU phần mềm: `-gpu swiftshader_indirect` và tăng RAM cho AVD.

### 3.3. Cài Appium và driver

```powershell
npm install -g appium
appium driver install uiautomator2
appium driver list --installed
```

Kết quả mong đợi: danh sách có `uiautomator2`.

### 3.4. Cài ứng dụng Swag Labs

Tải `Android.SauceLabs.Mobile.Sample.app.2.7.1.apk` từ trang Releases, sau đó:

```powershell
adb install -r "đường-dẫn\Android.SauceLabs.Mobile.Sample.app.2.7.1.apk"
```

Hoặc kéo thả trực tiếp file `.apk` vào giao diện máy ảo.

Kiểm tra app đã cài:

```powershell
adb shell pm list packages | findstr swaglabs
```

### 3.5. Cài thư viện Python

Tại thư mục gốc của repo:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 4. Cấu hình thiết bị

Chạy lệnh sau để lấy tên thiết bị:

```powershell
adb devices
```

Ví dụ:

```text
emulator-5554    device
```

Mở hai file sau và sửa `DEVICE_NAME` cho đúng với máy của bạn:

- `tuan-04/test_smoke.py`
- `tuan-05/test_login.py`

```python
APPIUM_SERVER = "http://127.0.0.1:4723"
DEVICE_NAME = "emulator-5554"
```

Nếu dùng điện thoại thật, `DEVICE_NAME` là mã máy hiện trong `adb devices`,
ví dụ `R58M123ABCD`.

## 5. Chạy bài kiểm thử

### 5.1. Khởi động Appium server

Mở **một terminal riêng** và giữ nguyên terminal này:

```powershell
appium
```

Nếu Appium báo thiếu driver:

```powershell
appium driver install uiautomator2
```

### 5.2. Chạy smoke test tuần 4

Tại thư mục gốc của repo:

```powershell
python tuan-04/test_smoke.py
```

Hoặc chạy bằng pytest:

```powershell
pytest tuan-04/test_smoke.py -v
```

Kết quả mong đợi:

```text
1. Đang kết nối Appium và mở ứng dụng Swag Labs...
2. Chờ màn hình đăng nhập hiện ra...
3. Đã thấy ô nhập tên đăng nhập, kiểm tra...
KẾT QUẢ: PASSED - ứng dụng mở được và có ô nhập tên đăng nhập
4. Đã đóng ứng dụng.
```

### 5.3. Chạy 3 test case Đăng nhập tuần 5

```powershell
pytest tuan-05/test_login.py -v
```

Kết quả mong đợi:

```text
tuan-05/test_login.py::test_dang_nhap_dung_vao_duoc_manh_products PASSED
tuan-05/test_login.py::test_dang_nhap_tai_khoan_bi_khoa           PASSED
tuan-05/test_login.py::test_dang_nhap_bi_trong_mat_khau           PASSED

3 passed
```

Chi tiết 3 test case nằm trong `tuan-05/testcases.md`.

> Nên chạy bằng `pytest` thay vì `python tuan-05/test_login.py`.
> Khi chạy trực tiếp bằng Python, nếu bài đầu lỗi thì các bài sau sẽ không chạy
> và không có bảng tổng kết 3 bài.

### 5.4. Chạy toàn bộ bài kiểm thử

```powershell
pytest -v
```

Lệnh này chạy cả smoke test tuần 4 và 3 test case tuần 5.

## 6. Nội dung kiểm thử tuần 5

| ID | Test case | Dữ liệu | Kết quả mong đợi | Hàm kiểm thử |
|---|---|---|---|---|
| TC-LOGIN-01 | Đăng nhập thành công | `standard_user` / `secret_sauce` | Vào màn hình PRODUCTS | `test_dang_nhap_dung_vao_duoc_manh_products` |
| TC-LOGIN-02 | Tài khoản bị khoá | `locked_out_user` / `secret_sauce` | Hiện `Sorry, this user has been locked out.` | `test_dang_nhap_tai_khoan_bi_khoa` |
| TC-LOGIN-03 | Bỏ trống mật khẩu | `standard_user` / *(trống)* | Hiện `Password is required` | `test_dang_nhap_bi_trong_mat_khau` |

Ảnh kết quả chạy nằm trong `tuan-05/anh/`:

- `01_dang_nhap_dung_vao_manh_PRODUCTS.png`
- `02_tai_khoan_bi_khoa.png`
- `03_bo_trong_mat_khau.png`

Kết quả đã kiểm chứng: **3/3 PASSED** trên emulator Android.

## 7. Nội dung tuần 6 – Trình bày vòng 1

Bộ slide trình bày vòng 1 (tối đa 8 trang) nằm trong `tuan-06/`:

- `slides.pdf` – bản nộp chính: kiểm thử tự động là gì, các cách tiếp cận, sơ đồ kiến trúc Appium do nhóm tự vẽ, giải phẫu một lệnh, demo 3 test case Đăng nhập và bài học.
- `slides.html` – bản nguồn để chỉnh sửa nội dung.
- `notes.md` – ghi chú tuần 6: trả lời câu hỏi phần đọc, góp ý nhận được và việc nhóm sẽ cải thiện.

Sau khi sửa `slides.html`, xuất lại PDF bằng Chrome:

```powershell
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --headless=new --no-pdf-header-footer --virtual-time-budget=8000 --print-to-pdf="$PWD\tuan-06\slides.pdf" "file:///$($PWD.Path.Replace('\','/'))/tuan-06/slides.html"
```

Hoặc mở `slides.html` bằng Chrome rồi **Ctrl+P → Save as PDF** (khổ ngang, tắt header/footer).

## 8. Lỗi thường gặp

| Lỗi | Nguyên nhân / cách sửa |
|---|---|
| `Connection refused` tới cổng 4723 | Chưa chạy `appium` ở terminal khác, hoặc Appium server đã dừng |
| `No device found` / `deviceName` sai | Chưa mở máy ảo, hoặc `adb devices` không thấy thiết bị |
| `Could not find a connected Android device` | Emulator bị tắt/treo giữa chừng; kiểm tra `adb devices`, khởi động lại emulator bằng Cold boot |
| Emulator treo, đứng hình | Thử Cold boot, dùng GPU phần mềm (`-gpu swiftshader_indirect`), tăng RAM cho AVD; không tắt emulator khi đang chạy test |
| `App not installed` | Chưa `adb install` file `.apk`, hoặc sai `appPackage` |
| `UiAutomator2 driver not installed` | Chạy `appium driver install uiautomator2` |
| `JAVA_HOME is not set` | Cài JDK 17 và đặt biến `JAVA_HOME`, mở lại terminal |
| `Element not found` quá 60 giây | App chưa load xong, hoặc accessibility id đã đổi → kiểm tra bằng Appium Inspector |
| `pytest: command not found` | Chưa kích hoạt `.venv` hoặc chưa `pip install -r requirements.txt` |

## 9. Ghi chú

- Ghi chú tuần 4: `tuan-04/notes.md`
- Ghi chú tuần 5: `tuan-05/notes.md`
- Ghi chú tuần 6: `tuan-06/notes.md`; slide: `tuan-06/slides.pdf`
- Tuần 7: chức năng 2 của nhóm A1 – sắp xếp sản phẩm (nộp trong `tuan-07/`).
- Khi gặp lỗi, ghi lại lỗi và cách sửa để đưa vào phần ghi chú tuần.
