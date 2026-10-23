"""
Tuần 5 - Bài kiểm thử chức năng Đăng nhập (nhóm App).

Mục tiêu: viết 3 bài kiểm thử cho màn hình đăng nhập của ứng dụng Swag Labs:
1. Đăng nhập đúng      -> vào được màn hình PRODUCTS (sau đó tự động đăng xuất)
2. Tài khoản bị khoá   -> hiện thông báo "Sorry, this user has been locked out."
3. Bỏ trống mật khẩu   -> hiện thông báo "Password is required"

Cách chạy:
    python3 test_login.py
"""

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Địa chỉ Appium server đang chạy trên máy
APPIUM_SERVER = "http://127.0.0.1:4723"

# UDID thiết bị
DEVICE_NAME = "emulator-5554"

# Thông tin tài khoản trong ứng dụng Swag Labs
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
    options.app_activity = "com.swaglabsmobileapp.MainActivity"

    # Giữ nguyên trạng thái để tránh lỗi quyền pm clear trên Android 15
    options.no_reset = True

    options.adb_exec_timeout = 120000
    options.new_command_timeout = 300

    return webdriver.Remote(APPIUM_SERVER, options=options)


def dong_app(driver):
    """Đóng ứng dụng an toàn."""
    try:
        driver.quit()
    except Exception:
        pass


def dang_xuat(driver):
    """Đăng xuất khỏi ứng dụng để đưa màn hình về lại trang Login (tránh kẹt ở Products)."""
    try:
        print("Đang thực hiện đăng xuất để dọn dẹp trạng thái...")
        # 1. Bấm nút Menu (3 gạch ngang)
        o_menu = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "test-Menu"))
        )
        o_menu.click()

        # 2. Bấm nút Logout trong menu
        o_logout = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "test-LOGOUT"))
        )
        o_logout.click()
        print("Đã đăng xuất thành công, về lại màn hình Login.")
    except Exception as e:
        print(f"Không thể đăng xuất tự động: {e}")


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
    """Đọc nội dung thông báo lỗi màu đỏ hiện trên màn hình đăng nhập."""
    o_khung_loi = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, "test-Error message"))
    )
    try:
        o_chu_loi = o_khung_loi.find_element(AppiumBy.XPATH, ".//android.widget.TextView")
        return o_chu_loi.text
    except Exception:
        return o_khung_loi.get_attribute("text") or ""


def test_dang_nhap_dung_vao_duoc_manh_products():
    """Bài 1: nhập đúng tài khoản thì vào được màn hình PRODUCTS."""
    print("\n--- Chạy bài 1: Đăng nhập đúng ---")
    driver = tao_driver()
    try:
        print("1. Nhập tên đăng nhập: " + TEN_DANG_NHAP)
        dien_ten_dang_nhap(driver, TEN_DANG_NHAP)

        print("2. Nhập mật khẩu")
        dien_mat_khau(driver, MAT_KHAU)

        print("3. Bấm nút LOGIN")
        bam_dang_nhap(driver)

        o_products = WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, "test-PRODUCTS"))
        )
        assert o_products.is_displayed(), "Không thấy màn hình PRODUCTS sau khi đăng nhập"

        print("KẾT QUẢ: PASSED - đăng nhập đúng và đã vào màn hình PRODUCTS")
    finally:
        # Đăng xuất để trả app về màn hình Login cho bài test sau
        dang_xuat(driver)
        dong_app(driver)


def test_dang_nhap_tai_khoan_bi_khoa():
    """Bài 2: tài khoản locked_out_user thì báo đã bị khoá."""
    print("\n--- Chạy bài 2: Tài khoản bị khóa ---")
    driver = tao_driver()
    try:
        print("1. Nhập tên đăng nhập bị khoá: " + TEN_DANG_NHAP_BI_KHOA)
        dien_ten_dang_nhap(driver, TEN_DANG_NHAP_BI_KHOA)

        print("2. Nhập mật khẩu")
        dien_mat_khau(driver, MAT_KHAU)

        print("3. Bấm nút LOGIN")
        bam_dang_nhap(driver)

        noi_dung = lay_noi_dung_loi(driver)
        assert "locked out" in noi_dung, f"Thông báo lỗi không đúng: {noi_dung}"

        print("KẾT QUẢ: PASSED - đã hiện thông báo tài khoản bị khoá: " + noi_dung)
    finally:
        dong_app(driver)


def test_dang_nhap_bi_trong_mat_khau():
    """Bài 3: bỏ trống mật khẩu thì báo 'Password is required'."""
    print("\n--- Chạy bài 3: Bỏ trống mật khẩu ---")
    driver = tao_driver()
    try:
        print("1. Nhập tên đăng nhập: " + TEN_DANG_NHAP)
        dien_ten_dang_nhap(driver, TEN_DANG_NHAP)

        # Đảm bảo ô mật khẩu hoàn toàn trống
        print("2. Để trống ô mật khẩu")
        o_mk = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "test-Password"))
        )
        o_mk.clear()

        print("3. Bấm nút LOGIN")
        bam_dang_nhap(driver)

        # Đọc thông báo lỗi (chờ tối đa 10 giây để UI kịp render chữ đỏ)
        noi_dung = lay_noi_dung_loi(driver)
        print(f"-> Thông báo lỗi thực tế nhận được trên app: '{noi_dung}'")
        
        assert "Password is required" in noi_dung, f"Thông báo lỗi không đúng: {noi_dung}"

        print("KẾT QUẢ: PASSED - đã hiện thông báo yêu cầu mật khẩu thành công!")
    finally:
        dong_app(driver)


if __name__ == "__main__":
    test_dang_nhap_dung_vao_duoc_manh_products()
    test_dang_nhap_tai_khoan_bi_khoa()
    test_dang_nhap_bi_trong_mat_khau()
