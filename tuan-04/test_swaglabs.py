"""
Tuần 4 - Bài kiểm thử đầu tiên trên app SwagLabs

Mục tiêu: mở ứng dụng Swag Labs trên máy ảo Android và kiểm tra
màn hình đăng nhập có ô nhập tên đăng nhập.

Cách chạy:
    python tuan-04/test_smoke.py
hoặc
    pytest tuan-04/test_smoke.py -v
"""

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Địa chỉ Appium server đang chạy trên máy
APPIUM_SERVER = "http://127.0.0.1:4723"

# Tên thiết bị, xem bằng lệnh: adb devices
DEVICE_NAME = "GYTGVC7D9PHI49CA"


def tao_driver():
    """Kết nối tới Appium server và mở ứng dụng Swag Labs."""
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = DEVICE_NAME
    options.app_package = "com.swaglabsmobileapp"
    options.app_activity = "com.swaglabsmobileapp.MainActivity"

    # Mỗi lần chạy bắt đầu từ trạng thái sạch (không còn đăng nhập từ lần trước).
    options.no_reset = True

    return webdriver.Remote(APPIUM_SERVER, options=options)

def test_mo_app_va_thay_o_nhap_ten_dang_nhap():
    # Bước 1: mở ứng dụng.
    print("1. Đang kết nối Appium và mở ứng dụng Swag Labs...")
    driver = tao_driver()

    try:
        # Bước 2: chờ tối đa 60 giây cho tới khi ô nhập tên đăng nhập hiện ra.
        # (Máy chậm hoặc lần chạy đầu tiên có thể mất gần 1 phút mới mở xong app.)
        # Ô này có nhãn "test-Username" do nhóm phát triển app gắn sẵn,
        # dùng nhãn sẽ ổn định hơn là dựa vào toạ độ trên màn hình.
        print("2. Chờ màn hình đăng nhập hiện ra...")
        o_username = WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, "test-Username"))
        )

        # Bước 3: kiểm tra ô nhập thực sự hiển thị trên màn hình.
        print("3. Đã thấy ô nhập tên đăng nhập, kiểm tra...")
        assert o_username.is_displayed(), "Không thấy ô nhập tên đăng nhập trên màn hình"

        print("KẾT QUẢ: PASSED - ứng dụng mở được và có ô nhập tên đăng nhập")
    finally:
        # Bước 4: đóng phiên làm việc, dù bài kiểm thử thành công hay thất bại.
        driver.quit()
        print("4. Đã đóng ứng dụng.")


if __name__ == "__main__":
    test_mo_app_va_thay_o_nhap_ten_dang_nhap()