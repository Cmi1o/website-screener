import constants

from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from app.driver_builder import options
from app.page import cursor, page_render_delay, PageDriver
from app.page.loading import prepare_page
from screenshots import screens_maker
from urls import next_page_url
from files_interactions import FilesManager


def main() -> None:
    url = 'https://www.wildberries.ru/seller/1158424'
    files_manager = FilesManager(page_url=url)
    
    with webdriver.Chrome(options) as driver:
        driver.get(url)
        
        page_driver = PageDriver(driver)
        
        if not files_manager.is_exist(constants.ASSETS_PATH):
            files_manager.create_new_folder(constants.ASSETS_PATH)
        
        pages_count = 1
        page_screens_count = 0
        screens_count = 0
        is_last_photo = False
        has_next_page = True
        
        prepare_page()
        cursor.accept_cookies(has_taskbar=False)
        cursor.remove_automatic_software_banner()
        cursor.move_to_top()
        
        while has_next_page:
            screen_height = page_driver.screen_size.height
            
            while page_screens_count < constants.MAX_SCREENS_COUNT and not is_last_photo:
                page_screens_count += 1
                screens_count += 1
                
                screens_maker.take_screenshot(url, screens_count)
                
                if not screens_count == 1:
                    if files_manager.compare_pngs(
                        screens_count - 1, screens_count
                    ) is True:
                        files_manager.delete_file(screens_count)
                        
                        is_last_photo = True
                        screens_count -= 1
                
                page_driver.scroll_down(screen_height * constants.PAGE_SCROLL_PERCENT)
                page_render_delay(1.5)
            
            if page_driver.is_next_page_button_found():
                pages_count += 1
                
                page_screens_count = 0
                is_last_photo = False
                
                page_driver.open_new_tab(
                    url=next_page_url(
                        base_url=url,
                        page_number=pages_count
                    )
                )
                prepare_page()
            
            else:
                has_next_page = False
    
    files_manager.create_new_docx()
    files_manager.switch_orientation(orientation='landscape')
    files_manager.fill_docx_by_dir_pngs(dir_path=constants.ASSETS_PATH)


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, WebDriverException) as error:
        if isinstance(error, WebDriverException):
            print('Network error')
