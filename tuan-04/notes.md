# Ghi chú tuần 4 – Cài đặt môi trường và smoke test

## 1. Mục tiêu

- Cài được môi trường kiểm thử tự động cho ứng dụng Android: Node.js, JDK 17, Android Studio, Appium, driver UiAutomator2, Python, Appium-Python-Client và pytest.
- Tạo máy ảo Android (AVD) và cài ứng dụng Swag Labs.
- Viết và chạy được bài kiểm thử đầu tiên `test_smoke.py`: mở app và kiểm tra có ô nhập tên đăng nhập.
- Hiểu được khi chạy một bài kiểm thử Appium thì máy tính và thiết bị làm những gì.

## 2. Công việc đã làm

- Cài Node.js, JDK 17, Android Studio và Python.
- Cài Appium, cài driver `uiautomator2`.
- Tạo máy ảo Android, khởi động máy ảo và kiểm tra bằng `adb devices`.
- Tải file `.apk` của Swag Labs và cài vào máy ảo.
- Tạo môi trường ảo Python, cài các thư viện trong `requirements.txt`.
- Viết `tuan-04/test_smoke.py` với các bước:
  - Kết nối tới Appium server.
  - Mở app Swag Labs.
  - Chờ ô nhập tên đăng nhập xuất hiện.
  - Kiểm tra ô nhập hiển thị.
  - Đóng phiên làm việc.
- Chạy bài kiểm thử thành công và chụp ảnh màn hình cho các thành viên.
- Ghi lại các lỗi gặp phải trong quá trình cài đặt và cách sửa.

## 3. Trả lời câu hỏi phần đọc

### Câu 1: Một script Appium gồm những bước nào? Mỗi bước ứng với dòng nào trong `test_smoke.py`?

Một script Appium thường gồm các bước: khởi tạo session → tìm hoặc chờ phần tử → thao tác với phần tử → kiểm tra kết quả → đóng session.


### Câu 2: Appium client, Appium server và driver UiAutomator2 lần lượt chạy ở đâu?

- **Appium client**: là đoạn code Python , chạy trên máy tính trong môi trường ảo `.venv`. Client gửi các lệnh HTTP tới Appium server.
- **Appium server**: là tiến trình Node.js chạy trên máy tính, mặc định ở `http://127.0.0.1:4723`. Server nhận lệnh từ client và chuyển tiếp cho driver.
- **Driver UiAutomator2**: là một plugin của Appium, được cài trong thư mục Appium trên máy tính. Driver này dùng ADB và UiAutomator2 để điều khiển ứng dụng đang chạy trên máy ảo hoặc điện thoại Android.
- **Ứng dụng Swag Labs**: chạy trên máy ảo Android (hoặc điện thoại thật), không chạy trên máy tính.

Có thể hình dung đường đi của một lệnh:

```text
Code Python (client)
        ↓ HTTP
Appium server (Node.js, cổng 4723)
        ↓
UiAutomator2 driver
        ↓ ADB / instrumentation
Máy ảo Android + app Swag Labs
```

### Câu 3: Bạn chọn cấu hình máy ảo (AVD) nào và vì sao?

Nhóm dùng máy ảo dạng Pixel có sẵn trong Android Studio, cấu hình khoảng 2 GB RAM, 4 CPU và hệ điều hành Android 13 trở lên (API 33+). Lý do:

- Cấu hình này đủ để cài và chạy app Swag Labs, không cần máy ảo quá nặng.
- Máy ảo có sẵn giúp tiết kiệm thời gian cài đặt.
- Nếu máy tính yếu, có thể dùng điện thoại Android thật để chạy nhanh hơn.


### Câu 4: Cài file `.apk` vào máy ảo bằng cách nào?

Kéo thả trực tiếp file `.apk` vào cửa sổ máy ảo Android.

Sau khi cài, kiểm tra lại bằng:

```powershell
adb shell pm list packages | findstr swaglabs
```

Kết quả mong đợi là thấy package `com.swaglabsmobileapp`.

## 4. Lỗi gặp và cách sửa

| Lỗi | Cách sửa |
|---|---|
| `Connection refused` tới cổng 4723 | Chưa chạy Appium server; mở terminal khác và chạy `appium` |
| `No device found` hoặc `deviceName` sai | Kiểm tra `adb devices`, khởi động máy ảo, sửa `DEVICE_NAME` cho đúng |
| `App not installed` | Chưa cài file `.apk` hoặc sai `appPackage` |
| `UiAutomator2 driver not installed` | Chạy `appium driver install uiautomator2` |
| `JAVA_HOME is not set` | Cài JDK 17, đặt biến `JAVA_HOME`, mở lại terminal |
| `Element not found` quá lâu | App chưa load xong hoặc sai accessibility id; kiểm tra bằng Appium Inspector và tăng thời gian chờ |
| Máy ảo bị treo hoặc `device offline` | Giữ máy ảo mở, kiểm tra `adb devices`, khởi động lại bằng Cold boot, tránh tắt máy ảo khi đang chạy test |

## 5. Điều mình học được

- Một bài kiểm thử Appium không chỉ là mở app rồi bấm, mà phải tạo session, chờ phần tử, thao tác, kiểm tra và đóng session đúng cách.
- Nên dùng **accessibility id** thay vì dựa vào tọa độ hoặc XPath dài, vì accessibility id ổn định hơn khi giao diện thay đổi.
- Nên dùng `WebDriverWait` thay cho `time.sleep` để chờ phần tử xuất hiện đúng lúc.
- `finally` rất quan trọng để đảm bảo app luôn được đóng, kể cả khi test thất bại.
- Cần phân biệt lỗi do code test và lỗi do môi trường (Appium server, máy ảo, ADB) để sửa đúng chỗ.

## 6. Ghi chú về việc dùng AI

- Nhóm có dùng AI để hỗ trợ giải thích kiến trúc Appium, cách chờ phần tử và cách xử lý một số lỗi môi trường.
- Câu trả lời của AI giúp hiểu nhanh hơn, nhưng nhóm đã kiểm tra lại bằng cách chạy test thực tế và đối chiếu với Appium Inspector.
- Có những nội dung AI gợi ý chưa sát với máy thật, ví dụ tên thiết bị và đường dẫn SDK, nên nhóm đã tự sửa theo `adb devices` và cấu hình máy.
- Bài học: không nên dán code hoặc câu trả lời của AI mà không chạy thử; phải hiểu và chỉnh lại cho đúng môi trường của mình.
