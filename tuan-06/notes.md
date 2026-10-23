# Ghi chú tuần 6 – Trình bày vòng 1 (Nhóm A1)

## 1. Mục tiêu và việc đã làm

- Trình bày bằng lời của nhóm: kiểm thử tự động là gì, vì sao cần, khi nào không nên dùng và các cách tiếp cận phổ biến.
- Vẽ sơ đồ kiến trúc Appium của nhóm: **client → Appium server → UiAutomator2 driver → ADB / instrumentation → thiết bị Android + Swag Labs**.
- Giải thích đường đi của một lệnh cụ thể: tìm ô `test-Username`, nhập `standard_user` và bấm `test-LOGIN`.
- Demo 3 test case Đăng nhập bằng `pytest tuan-05/test_login.py -v` (3/3 PASSED, khoảng 46 giây).
- Làm slide trình bày tối đa 8 trang, có sơ đồ kiến trúc do nhóm tự vẽ: `tuan-06/slides.pdf` (bản HTML nguồn: `tuan-06/slides.html`).

## 2. Trả lời câu hỏi phần đọc

### Câu 1: WebDriver khác Selenium IDE và Selenium Grid ở đâu?

| Thành phần | Bản chất | Dùng khi nào |
|---|---|---|
| **Selenium IDE** | Công cụ ghi và phát lại thao tác trên trình duyệt, không cần viết code. | Học thử, kiểm tra nhanh một luồng; không phù hợp để bảo trì lâu dài. |
| **WebDriver** | Thư viện/API cho phép viết code điều khiển trình duyệt, chạy được nhiều trình duyệt và tích hợp với pytest, CI. | Viết bộ kiểm thử tự động thực sự, cần độ ổn định và khả năng bảo trì. |
| **Selenium Grid** | Hạ tầng chạy phân tán: chia bài kiểm thử ra nhiều máy/trình duyệt cùng lúc. | Bộ test lớn, cần chạy song song trên nhiều môi trường. |

Tóm lại: **IDE là công cụ ghi thao tác, WebDriver là cách viết code để điều khiển trình duyệt, còn Grid là hạ tầng để chạy nhiều WebDriver cùng lúc** — ba thứ không thay thế nhau.

### Câu 2: Vẽ lại đường đi của một lệnh (từ code tới thiết bị)

```text
Code Python (client, chạy trên máy tính)
        │  lệnh W3C qua HTTP
        ▼
Appium Server (Node.js, http://127.0.0.1:4723)
        │  chọn driver theo session
        ▼
UiAutomator2 Driver (chạy trên máy tính)
        │  ADB / instrumentation
        ▼
Thiết bị Android + app Swag Labs
```

Chiều ngược lại, kết quả (element id, text, trạng thái) đi từ thiết bị về driver, về client. Hiểu đường đi này giúp khoanh vùng lỗi nhanh: `Connection refused` là lỗi server, `device not found` là lỗi thiết bị/ADB, còn `element not found` thường là lỗi locator hoặc chờ chưa đúng.

Với web (Selenium), đường đi tương tự nhưng thay vì Appium server + UiAutomator2 Driver thì client nói chuyện với **browser driver** (ví dụ ChromeDriver), rồi ChromeDriver điều khiển trình duyệt.

### Câu 3: Vì sao kiểm thử qua giao diện nên ít và có chọn lọc?

- UI test chạy **chậm**, cần khởi động app/trình duyệt, thiết bị.
- Dễ **flaky**: phụ thuộc thời điểm render, mạng, trạng thái thiết bị.
- **Đắt** khi bảo trì: giao diện đổi là phải sửa locator và luồng thao tác.
- Theo **test pyramid**, nên dành phần lớn bài kiểm thử cho unit và integration; UI/E2E chỉ dùng cho các luồng quan trọng nhất của người dùng.
- Với Swag Labs, nhóm chọn 3 test case Đăng nhập và 2 chức năng quan trọng thay vì cố kiểm tra mọi màn hình.

## 3. Góp ý nhận được


## 4. Điều nhóm sẽ cải thiện

## 5. Ghi chú về việc dùng AI

- Nhóm dùng AI để gợi ý dàn ý slide, gợi ý cách vẽ sơ đồ kiến trúc và soát lại nội dung ghi chú.
- Nội dung AI gợi ý được nhóm đối chiếu lại với tài liệu Appium/Selenium/pytest và với code thật trong `tuan-05/test_login.py`.
- Phần chạy demo, số liệu 3/3 PASSED và ảnh minh chứng do nhóm tự chạy trên emulator; không lấy từ AI.
- Bài học: AI giúp tiết kiệm thời gian chuẩn bị khung, nhưng phải tự kiểm tra lại bằng tài liệu chính thức và kết quả chạy thật.

## 6. Việc tiếp theo (chuẩn bị tuần 7)

- Chức năng 2 của nhóm **A1: Sắp xếp sản phẩm** trên Swag Labs.
- Làm thí nghiệm theo yêu cầu: bấm LOGIN rồi tìm ngay màn Products **không dùng wait** để thấy lỗi chập chờn, sau đó thêm `WebDriverWait` và ghi lại nhận xét.
- Viết 2–3 test case, có ít nhất 1 trường hợp sai; không dùng `time.sleep`.
- Nộp vào `tuan-07/`: `test_sap_xep_san_pham.py`, `testcases.md`, `notes.md`.

## 7. Đường dẫn liên quan

- Slide: `tuan-06/slides.pdf`
- Bộ test demo: `tuan-05/test_login.py`
- Test case viết bằng lời: `tuan-05/testcases.md`
- Ảnh minh chứng: `tuan-05/anh/`
