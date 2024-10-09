from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


__all__ = (
    'is_next_page_button_found',
)


def is_next_page_button_found(driver: WebDriver) -> bool:
    try:
        return bool(driver.find_element(
            By.XPATH, '//*[@id="catalog"]/div[6]/div/a[3]'
        ))
    except NoSuchElementException:
        return False