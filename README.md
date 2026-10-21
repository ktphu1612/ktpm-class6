# KTPM - Nhóm App (Appium + Swag Labs)

Bài thực hành kiểm thử tự động tuần 4 trên ứng dụng **Swag Labs** (Android),
dùng **Appium 2 + UiAutomator2**, viết bằng **Python + pytest**.

- Ứng dụng: Swag Labs, tải `.apk` tại
  <https://github.com/saucelabs/sample-app-mobile/releases>
- Tài khoản: `standard_user` / `secret_sauce`

## Cấu trúc kho mã

```
.
├─ requirements.txt     # thư viện Python cần cài
├─ tuan-04/
│  ├─ test_smoke.py     # bài kiểm thử đầu tiên (1 file duy nhất, tự chạy)
│  ├─ notes.md          # ghi chú của từng thành viên
│  └─ anh/              # ảnh chụp màn hình chạy thành công
└─ README.md
```

## 1. Cài đặt môi trường

### 1.1. Phần mềm bắt buộc

| Phần mềm | Phiên bản | Kiểm tra |
|---|---|---|
| Node.js | 18 trở lên | `node -v` |
| JDK | 17 | `java -version` |
| Android Studio | mới nhất | có `adb` trong `platform-tools` |
| Python | 3.10 trở lên | `python --version` |

Thêm biến môi trường (Windows):

- `JAVA_HOME` → thư mục cài JDK 17
- `ANDROID_HOME` → `%LOCALAPPDATA%\Android\Sdk`
- Thêm vào `PATH`: `%ANDROID_HOME%\platform-tools` và `%ANDROID_HOME%\emulator`

Mở terminal mới rồi kiểm tra: `java -version`, `adb devices`.

### 1.2. Tạo máy ảo Android (AVD)
Lưu ý: Khi cài **SDK Manager** mặc định **Android Studio** sẽ cài 1 máy ảo trên máy bạn, nếu có thể chạy máy ảo đó
thì không cần thiết cài thêm máy ảo nào khác, đỡ nặng máy

Android Studio → **Device Manager** → **Create Virtual Device** → chọn Pixel 5
(hoặc tương tự) → hệ điều hành **API 33+** → Finish → bấm ▶ để khởi động.

Máy yếu có thể dùng điện thoại Android thật: bật **USB debugging**, cắm cáp,
rồi sau đó dùng lệnh `adb devices` để lấy mã thiết bị.

### 1.3. Cài Appium và driver

```powershell
npm install -g appium
appium driver install uiautomator2
appium driver list --installed ##phải thấy được uiautomator đã tải
```

### 1.4. Cài ứng dụng Swag Labs

Tải `Android.SauceLabs.Mobile.Sample.app.2.7.1.apk` từ trang Releases, sau đó:

```powershell
adb install -r "đường-dẫn\Android.SauceLabs.Mobile.Sample.app.2.7.1.apk"
```
hoặc kéo thả trực tiếp vào giao diện máy ảo của bạn.

### 1.5. Cài thư viện Python

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 2. Chạy bài kiểm thử

Mở **một terminal riêng** và chạy Appium server (giữ nguyên terminal này):

```powershell
appium
```

Terminal khác, tại thư mục gốc của kho mã:

```powershell
python tuan-04/test_smoke.py
```

Kết quả mong đợi:

```
1. Đang kết nối Appium và mở ứng dụng Swag Labs...
2. Chờ màn hình đăng nhập hiện ra...
3. Đã thấy ô nhập tên đăng nhập, kiểm tra...
KẾT QUẢ: PASSED - ứng dụng mở được và có ô nhập tên đăng nhập
4. Đã đóng ứng dụng.
```

## 3. Đổi máy / đổi thiết bị

Mở `tuan-04/test_smoke.py` và sửa 2 dòng ở đầu file cho đúng với máy của bạn:

```python
APPIUM_SERVER = "http://127.0.0.1:4723"   # địa chỉ Appium server
DEVICE_NAME = "emulator-5554"             # lấy từ lệnh: adb devices
```

Dùng điện thoại thật thì `DEVICE_NAME` là mã máy hiện trong `adb devices`,
ví dụ `R58M123ABCD`.


## 5. Lỗi thường gặp

| Lỗi | Nguyên nhân / cách sửa |
|---|---|
| `Connection refused` tới cổng 4723 | Chưa chạy `appium` ở terminal khác |
| `No device found` / `deviceName` sai | Chưa mở máy ảo, hoặc `adb devices` không thấy thiết bị |
| `App not installed` | Chưa `adb install` file `.apk`, hoặc sai `appPackage` |
| `UiAutomator2 driver not installed` | Chạy `appium driver install uiautomator2` |
| `JAVA_HOME is not set` | Cài JDK 17 và đặt biến `JAVA_HOME`, mở lại terminal |
| `Element not found` quá 60 giây | App chưa load xong, hoặc accessibility id đã đổi → kiểm tra bằng Appium Inspector |

