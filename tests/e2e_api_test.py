from main import PROMPT_FILE
from utils.file_utils import read_file, write_file
from utils.api_utils import generate_part, generate_full_conspect
from openai import OpenAI
from dotenv import load_dotenv
import os
from colorlog import ColoredFormatter

load_dotenv()

PROMPT_FILE = "tests/assets/e2e_prompt_file.md"
TASK_FILE = "tests/assets/e2e_task_file.md"

POLZA_API_KEY = os.getenv("POLZA_API_KEY")

def e2e_full_conspect_test():
    client = OpenAI(base_url="https://polza.ai/api/v1")

    # Читаем файл с промптом и задачи
    prompt = read_file(PROMPT_FILE)
    task = read_file(TASK_FILE)

    # Генерируем полный контекст
    conspect = generate_full_conspect(client, prompt, task)

    # Записываем результат в файл
    write_file("e2e_full_conspect.md", "|".join(conspect))

    # Проверка что в файле есть слово обезьянка и слоник
    result = read_file("e2e_full_conspect.md")
    assert "обезьянка" in result and "слоник" in result, "Файл не содержит слова обезьянка и слоника"




