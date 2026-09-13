# uv add load_dotenv

from dotenv import load_dotenv
from os import getenv
from utils.file_utils import read_file, write_file
from utils.api_utils import generate_part, generate_full_conspect
from openai import OpenAI
import logging
from logging.handlers import RotatingFileHandler

# uv add colorlog
from colorlog import ColoredFormatter



# Обработчик терминала
console_handler = logging.StreamHandler()

# Цветной форматтер для терминала
# Цветной форматтер
console_formatter = ColoredFormatter(
    fmt=(
        "%(asctime)s | %(log_color)s%(levelname)-8s%(reset)s | %(name)s | %(log_color)s%(message)s"
    ),
    datefmt="%H:%M:%S",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_white,bg_red",
    },
)

console_handler.setFormatter(console_formatter)


logging.basicConfig(
    level=logging.DEBUG,  # Что будет логироваться. DEBUG - все сообщения, INFO - только информационные и выше, WARNING - предупреждения и выше, ERROR - ошибки и выше, CRITICAL - только критические ошибки
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",  # Как вообще лог строка форматируется
    datefmt="%Y-%m-%d %H:%M:%S",  # Как форматируется дата
    handlers=[
        console_handler,  # вывод в терминал
        RotatingFileHandler(
            "app.log", maxBytes=1024 * 1024 * 2, backupCount=3, encoding="utf-8"
        ),  # вывод в файл с ротацией
    ],
)

load_dotenv()

POLZA_API_KEY = getenv("POLZA_API_KEY")
IS_IMAGE = getenv("IS_PAID") == "True"

PROMPT_FILE = getenv("PROMPT_FILE")
TASK_FILE = getenv("TASK_FILE")


if __name__ == "__main__":
    logging.debug("Приложение начало свою работу")
    if not POLZA_API_KEY:
        logging.critical("Не найден ключ от API")
        raise ValueError(
            "Не найден ключ API. Пожалуйста, установите переменную окружения POLZA_API_KEY."
        )
    if not PROMPT_FILE:
        logging.critical("Не найдена ссылка на промпт файл")
        raise ValueError(
            "Не найден файл с промптом. Пожалуйста, установите переменную окружения PROMPT_FILE."
        )
    if not TASK_FILE:
        logging.critical("Не найдена ссылка на файл задачи")
        raise ValueError(
            "Не найден файл с задачами. Пожалуйста, установите переменную окружения TASK_FILE."
        )

    task_file = read_file(TASK_FILE)
    prompt_file = read_file(PROMPT_FILE)
    client = OpenAI(api_key=POLZA_API_KEY, base_url="https://polza.ai/api/v1")

    conspect = generate_full_conspect(client, prompt_file, task_file)
    write_file("conspect.md", "\n++++++\n".join(conspect))
    logging.debug("Приложение закончило свою работу")
