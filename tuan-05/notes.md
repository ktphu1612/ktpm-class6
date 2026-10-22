# Ghi chú tuần 5 – Kiểm thử chức năng Đăng nhập

## 1. Mục tiêu

- Hiểu và làm được 3 việc cốt lõi của kiểm thử giao diện: tìm đúng phần tử, thao tác với phần tử và kiểm tra kết quả.
- Viết được 3 test case cho chức năng Đăng nhập của app Swag Labs:
  1. Đăng nhập đúng thì vào màn hình PRODUCTS.
  2. Tài khoản bị khoá thì hiện thông báo lỗi.
  3. Bỏ trống mật khẩu thì hiện thông báo `Password is required`.
- Biết dùng accessibility id, `send_keys`, `click`, `WebDriverWait` và `assert`.

## 2. Công việc đã làm

- Viết 3 test case bằng lời trong `tuan-05/testcases.md`.
- Dùng Appium Inspector để kiểm tra accessibility id của các phần tử trên màn hình đăng nhập.
- Viết `tuan-05/test_login.py` gồm 3 bài kiểm thử:
  - `test_dang_nhap_dung_vao_duoc_manh_products`
  - `test_dang_nhap_tai_khoan_bi_khoa`
  - `test_dang_nhap_bi_trong_mat_khau`
- Tách các thao tác dùng chung thành hàm: mở app, nhập tên đăng nhập, nhập mật khẩu, bấm LOGIN, đọc thông báo lỗi, đóng app.
- Chạy cả 3 bài bằng pytest, chụp ảnh kết quả và lưu vào `tuan-05/anh/`.
- Ghi lại các lỗi gặp phải, đặc biệt là lỗi máy ảo bị treo hoặc mất kết nối giữa chừng.

## 3. Trả lời câu hỏi phần đọc

### Câu 1: Với ô tên đăng nhập ở trang `/login`, nên xác định bằng cách nào là ổn định nhất, vì sao?

- Với web, nên dùng `id` nếu có, sau đó đến `name` hoặc CSS selector ngắn gọn. `id` ổn định vì nó gắn trực tiếp với phần tử và ít bị thay đổi khi giao diện đổi bố cục.
- Không nên dùng XPath tuyệt đối hoặc tọa độ, vì giao diện thay đổi là test sẽ hỏng ngay.
- Với app Android, nhóm dùng **accessibility id** `test-Username`. Đây là id do nhóm phát triển app gắn sẵn, không phụ thuộc vào vị trí hay cấu trúc cây giao diện.

### Câu 2: Muốn nhập chữ vào một ô thì dùng lệnh gì?

Dùng `send_keys`:

```python
o_ten.clear()
o_ten.send_keys("standard_user")
```

Trong đó `o_ten` là phần tử ô nhập. Nên gọi `clear()` trước khi nhập để tránh trường hợp ô đã có sẵn nội dung từ lần chạy trước.

### Câu 3: Làm thế nào để biết id của một ô nhập trên trang?

- Với web: mở Chrome DevTools → tab **Elements** → chọn ô nhập → xem thuộc tính `id`, `name` hoặc `class`.
- Với app Android: mở **Appium Inspector**, tạo session với app Swag Labs, chọn phần tử trên màn hình rồi xem `accessibility id` hoặc `resource-id`.

### Câu 4: Vì sao trên điện thoại nên ưu tiên accessibility id?

- Accessibility id thường do nhóm phát triển app gắn sẵn nên ổn định hơn XPath hay tọa độ.
- Nó dễ đọc, dễ hiểu và ít bị thay đổi khi bố cục màn hình thay đổi.
- UiAutomator2 hỗ trợ tìm phần tử theo accessibility id rất tốt.
- Cùng một id có thể dùng cho nhiều kích thước màn hình và nhiều thiết bị khác nhau.

### Câu 5: Nếu kết quả thực tế khác mong đợi thì pytest báo gì?

Pytest sẽ báo bài kiểm thử **FAILED**, in ra `AssertionError`, nội dung thông báo lỗi mình đặt trong `assert`, và vị trí dòng code gây lỗi. Nếu dùng `pytest -v`, phần tổng kết sẽ hiển thị số bài đã pass và fail.

Ví dụ:

```python
assert "Password is required" in noi_dung, f"Thông báo lỗi không đúng: {noi_dung}"
```

Nếu thông báo thực tế khác, pytest sẽ hiện nội dung `Thông báo lỗi không đúng: ...` để mình biết cần sửa gì.

## 4. Kỹ thuật đã dùng trong `test_login.py`

- Dùng `AppiumBy.ACCESSIBILITY_ID` để tìm:
  - `test-Username`
  - `test-Password`
  - `test-LOGIN`
  - `test-PRODUCTS`
  - `test-Error message`
- Dùng `WebDriverWait` với các điều kiện:
  - `presence_of_element_located` khi chỉ cần phần tử có trong cây giao diện.
  - `visibility_of_element_located` khi cần phần tử hiển thị rõ trên màn hình.
  - `element_to_be_clickable` khi cần bấm nút.
- Dùng `clear()` và `send_keys()` để nhập dữ liệu.
- Dùng `click()` để bấm nút LOGIN.
- Dùng `assert` để kiểm tra:
  - Màn hình PRODUCTS hiển thị sau khi đăng nhập đúng.
  - Thông báo tài khoản bị khoá có chứa `locked out`.
  - Thông báo thiếu mật khẩu có chứa `Password is required`.
- Dùng `finally` và hàm `dong_app()` để đóng app dù test thành công hay thất bại.
- Không dùng `time.sleep`; tất cả đều chờ bằng `WebDriverWait`.

### Một lỗi kỹ thuật đáng chú ý

Khung thông báo lỗi có accessibility id `test-Error message`, nhưng đây là một `ViewGroup` nên `.text` của nó bị rỗng. Chữ thông báo thật nằm trong một `TextView` con. Vì vậy phải tìm phần tử con:

```python
o_khung_loi = WebDriverWait(driver, 30).until(
    EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, "test-Error message"))
)
o_chu_loi = o_khung_loi.find_element(AppiumBy.XPATH, ".//android.widget.TextView")
noi_dung = o_chu_loi.text
```

Nếu chỉ đọc `.text` của khung lỗi thì sẽ không thấy nội dung và test dễ bị sai.

## 5. Kết quả chạy

Chạy bằng lệnh:

```cmd
pytest tuan-05/test_login.py -v
```

Kết quả:

```text
tuan-05/test_login.py::test_dang_nhap_dung_vao_duoc_manh_products PASSED
tuan-05/test_login.py::test_dang_nhap_tai_khoan_bi_khoa           PASSED
tuan-05/test_login.py::test_dang_nhap_bi_trong_mat_khau           PASSED

3 passed in 45.78s
```

Ảnh minh chứng nằm trong `tuan-05/anh/`:

- `01_dang_nhap_dung_vao_manh_PRODUCTS.png`
- `02_tai_khoan_bi_khoa.png`
- `03_bo_trong_mat_khau.png`

## 6. Lỗi gặp và cách sửa

| Lỗi | Nguyên nhân / cách sửa |
|---|---|
| Không đọc được nội dung lỗi vì `.text` rỗng | `test-Error message` là `ViewGroup`; phải lấy `TextView` con bên trong |
| `Element not found` | Sai accessibility id hoặc app chưa load xong; kiểm tra bằng Appium Inspector, tăng thời gian chờ |
| `device offline` / `Could not find a connected Android device` | Máy ảo bị treo hoặc bị tắt giữa chừng; kiểm tra `adb devices`, khởi động lại máy ảo bằng Cold boot, giữ máy ảo mở |
| Appium server dừng giữa chừng | Kiểm tra terminal chạy `appium`, khởi động lại server và chạy lại test |
| Test chạy lúc được lúc không | Thường do máy ảo chưa ổn định hoặc chờ chưa đúng; dùng `WebDriverWait`, tránh `time.sleep`, chạy lại trên máy ảo sạch |

Lưu ý: lỗi máy ảo treo/offline là lỗi môi trường, không phải lỗi logic của test. Khi gặp, cần kiểm tra `adb devices` và trạng thái Appium server trước khi sửa code.

## 7. Điều mà bọn em học được

- Tìm phần tử bằng accessibility id ổn định hơn nhiều so với dùng tọa độ hoặc XPath dài.
- `WebDriverWait` giúp test chờ đúng lúc thay vì chờ mò bằng `time.sleep`.
- Mỗi bài test nên bắt đầu từ trạng thái sạch để tránh ảnh hưởng lẫn nhau.
- `assert` cần có thông báo lỗi rõ ràng để khi fail biết ngay sai ở đâu.
- Phải kiểm tra cấu trúc cây giao diện (ViewGroup/TextView) để lấy đúng dữ liệu.
- Cần phân biệt lỗi code với lỗi môi trường như máy ảo treo, Appium server dừng hay ADB mất kết nối.

## 8. Ghi chú về việc dùng AI

- Nhóm có dùng AI để hỗ trợ giải thích cách tìm phần tử, cách dùng `WebDriverWait`, cách đọc thông báo lỗi trong `ViewGroup` và cách xử lý lỗi máy ảo/ADB.
- Câu trả lời của AI giúp hiểu nhanh hơn, nhưng nhóm đã kiểm tra lại bằng cách chạy test thật và xem kết quả trên Appium Inspector.
- Có nội dung AI gợi ý chưa sát với app thật, ví dụ phải lấy `TextView` con thay vì đọc `.text` của khung lỗi; nhóm đã sửa sau khi kiểm tra.
- Bài học: AI chỉ là công cụ hỗ trợ; phải tự chạy, tự đọc log và hiểu code thì mới sửa được lỗi đúng.
