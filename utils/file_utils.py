"""
Модуль содержащий утилиты для работы с файлами
- read_file
- write_file
"""
import logging
logger = logging.getLogger(__name__)


def read_file(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            logger.debug(f"Файл {file_path} успешно прочитан")
            return file.read()

    except FileNotFoundError:

        logger.error(f"Файл {file_path} не найден")
        raise


def write_file(file_path: str, content: str) -> None:
    try:
        logger.debug(f"Начинается запись в файл {file_path}")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        logger.debug(f"Файл {file_path} успешно записан")
    except Exception as e:
        logger.error(f"Ошибка при записи в файл {file_path}: {e}")
        raise
