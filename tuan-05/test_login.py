"""
Tuần 5 - Bài kiểm thử chức năng Đăng nhập (nhóm App).

Mục tiêu: viết 3 bài kiểm thử cho màn hình đăng nhập của ứng dụng Swag Labs:
    1. Đăng nhập đúng      -> vào được màn hình PRODUCTS
    2. Tài khoản bị khoá   -> hiện thông báo "Sorry, this user has been locked out."
    3. Bỏ trống mật khẩu   -> hiện thông báo "Password is required"

Cách chạy (đứng ở thư mục gốc của kho mã):
    python tuan-05/test_login.py

Muốn chạy bằng pytest cũng được:
    pytest tuan-05/test_login.py -v
"""

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Địa chỉ Appium server đang chạy trên máy của bạn.
APPIUM_SERVER = "http://127.0.0.1:4723"

# Tên thiết bị, xem bằng lệnh: adb devices
DEVICE_NAME = "emulator-5554"

# Thông tin tài khoản trong ứng dụng Swag Labs.
TEN_DANG_NHAP = "standard_user"
MAT_KHAU = "secret_sauce"
TEN_DANG_NHAP_BI_KHOA = "locked_out_user"

def tao_driver():
    """Kết nối tới Appium server và mở ứng dụng Swag Labs."""
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = DEVICE_NAME
    options.app_package = "com.swaglabsmobileapp"
    options.app_activity = ".MainActivity"

    # Mỗi lần chạy bắt đầu từ trạng thái sạch (không còn đăng nhập từ lần trước).
    options.no_reset = False

    # Cho phép chờ lâu hơn khi giao tiếp với máy ảo (máy yếu hay bị timeout).
    options.adb_exec_timeout = 120000
    options.new_command_timeout = 300

    return webdriver.Remote(APPIUM_SERVER, options=options)


def dong_app(driver):
    """Đóng ứng dụng.

    Máy ảo đôi lúc bị treo làm lệnh đóng app lỗi; lỗi lúc đóng không quan trọng
    nên bỏ qua để bài kiểm thử không bị dừng bởi lỗi dọn dẹp.
    """
    try:
        driver.quit()
    except Exception:
        pass


def dien_ten_dang_nhap(driver, ten_dang_nhap):
    """Nhập tên đăng nhập vào ô Username."""
    o_ten = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "test-Username"))
    )
    o_ten.clear()
    o_ten.send_keys(ten_dang_nhap)


def dien_mat_khau(driver, mat_khau):
    """Nhập mật khẩu vào ô Password."""
    o_mk = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "test-Password"))
    )
    o_mk.clear()
    o_mk.send_keys(mat_khau)


def bam_dang_nhap(driver):
    """Bấm nút LOGIN."""
    o_nut = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "test-LOGIN"))
    )
    o_nut.click()


def lay_noi_dung_loi(driver):
    """Đọc nội dung thông báo lỗi màu đỏ hiện trên màn hình đăng nhập.

    Lưu ý: "test-Error message" chỉ là khung đỏ (ViewGroup) nên .text của nó rỗng.
    Chữ thông báo thật nằm ở TextView bên trong khung, nên phải lấy phần tử con.
    """
    o_khung_loi = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, "test-Error message"))
    )
    o_chu_loi = o_khung_loi.find_element(AppiumBy.XPATH, ".//android.widget.TextView")
    return o_chu_loi.text


def test_dang_nhap_dung_vao_duoc_manh_products():
    """Bài 1: nhập đúng tài khoản thì vào được màn hình PRODUCTS (danh sách sản phẩm)."""
    print("1. Mở ứng dụng Swag Labs")
    driver = tao_driver()
    try:
        print("2. Nhập tên đăng nhập: " + TEN_DANG_NHAP)
        dien_ten_dang_nhap(driver, TEN_DANG_NHAP)

        print("3. Nhập mật khẩu")
        dien_mat_khau(driver, MAT_KHAU)

        print("4. Bấm nút LOGIN")
        bam_dang_nhap(driver)

        # Chờ tới khi màn hình PRODUCTS hiện ra rồi kiểm tra nó thực sự hiển thị.
        o_products = WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, "test-PRODUCTS"))
        )
        assert o_products.is_displayed(), "Không thấy màn hình PRODUCTS sau khi đăng nhập"

        print("KẾT QUẢ: PASSED - đăng nhập đúng và đã vào màn hình PRODUCTS")
    finally:
        dong_app(driver)


def test_dang_nhap_tai_khoan_bi_khoa():
    """Bài 2: tài khoản locked_out_user thì báo đã bị khoá, không vào được."""
    print("1. Mở ứng dụng Swag Labs")
    driver = tao_driver()
    try:
        print("2. Nhập tên đăng nhập bị khoá: " + TEN_DANG_NHAP_BI_KHOA)
        dien_ten_dang_nhap(driver, TEN_DANG_NHAP_BI_KHOA)

        print("3. Nhập mật khẩu")
        dien_mat_khau(driver, MAT_KHAU)

        print("4. Bấm nút LOGIN")
        bam_dang_nhap(driver)

        # Kiểm tra thông báo lỗi hiện ra có đúng nội dung không.
        noi_dung = lay_noi_dung_loi(driver)
        assert "locked out" in noi_dung, f"Thông báo lỗi không đúng: {noi_dung}"

        print("KẾT QUẢ: PASSED - đã hiện thông báo tài khoản bị khoá: " + noi_dung)
    finally:
        dong_app(driver)


def test_dang_nhap_bi_trong_mat_khau():
    """Bài 3: bỏ trống mật khẩu thì báo 'Password is required'."""
    print("1. Mở ứng dụng Swag Labs")
    driver = tao_driver()
    try:
        print("2. Nhập tên đăng nhập, để trống mật khẩu: " + TEN_DANG_NHAP)
        dien_ten_dang_nhap(driver, TEN_DANG_NHAP)

        print("3. Bấm nút LOGIN")
        bam_dang_nhap(driver)

        # Kiểm tra thông báo lỗi hiện ra có đúng nội dung không.
        noi_dung = lay_noi_dung_loi(driver)
        assert "Password is required" in noi_dung, f"Thông báo lỗi không đúng: {noi_dung}"

        print("KẾT QUẢ: PASSED - đã hiện thông báo yêu cầu mật khẩu: " + noi_dung)
    finally:
        dong_app(driver)


if __name__ == "__main__":
    # Chạy trực tiếp bằng lệnh python thì gọi lần lượt từng bài kiểm thử.
    test_dang_nhap_dung_vao_duoc_manh_products()
    test_dang_nhap_tai_khoan_bi_khoa()
    test_dang_nhap_bi_trong_mat_khau()
