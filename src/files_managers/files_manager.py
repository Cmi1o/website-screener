import os

from imagehash import dhash
from PIL import Image

import constants


class FilesManager:
    def __init__(self, *, page_url: str) -> None:
        self._source_page_url = page_url

    @staticmethod
    def _abs_path(file_path: str) -> str:
        return os.path.abspath(file_path)

    def _get_photo_path(self, photo_serial_number: int) -> str:
        return constants.SCREENSHOT_PATH.format(
            hash(self._source_page_url), photo_serial_number
        )

    def delete_file(self, photo_serial_number: int) -> None:
        os.remove(self._get_photo_path(photo_serial_number))

    def create_new_folder(self, path: str) -> None:
        os.mkdir(self._abs_path(path))

    def is_exist(self, path: str) -> bool:
        return os.path.exists(self._abs_path(path))

    def compare_pngs(
        self, first_serial_number: int, second_serial_number: int
    ) -> bool:
        first_path = self._get_photo_path(first_serial_number)
        second_path = self._get_photo_path(second_serial_number)

        return dhash(Image.open(first_path)) == dhash(Image.open(second_path))
