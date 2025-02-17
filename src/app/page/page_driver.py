from typing import NamedTuple

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class ScreenSizes(NamedTuple):
    width: int | float
    height: int | float


class PageDriver:
    def __init__(self, driver: WebDriver) -> None:
        self.__driver = driver

    def open_new_tab(self, url: str) -> None:
        body = self.__driver.find_element(By.TAG_NAME, 'body')

        body.send_keys(Keys.CONTROL + 't')  # open new tab
        self.__driver.get(url)

    def is_next_page_button_found(self) -> bool:
        try:
            return bool(
                self.__driver.find_element(
                    By.LINK_TEXT, 'Следующая страница'  # if russian language
                )
            )
        except NoSuchElementException:
            return False

    @property
    def screen_sizes(self) -> ScreenSizes:
        sizes = self.__driver.get_window_size()

        return ScreenSizes(width=sizes['width'], height=sizes['height'])

    def scroll_down(self, step: float = 515) -> None:
        self.__driver.execute_script(f'window.scrollBy(0, {step})')
