from unittest import result

from openai import OpenAI
import logging

logger = logging.getLogger(__name__)


def generate_part(
    client: OpenAI, prompt: str, full_task: str, current_part: str
) -> str | None:
    logger.debug(f"Начинается запрос к модели google/gemini-2.5-flash-lite")

    PROMPT = f"""
    Ты выполнляешь глобальную задачу: {prompt}
    Ты движешься по плану: {full_task}
    Твоя текущая задача: {current_part}"""

    completion = client.chat.completions.create(
        model="google/gemini-2.5-flash-lite",
        messages=[{"role": "user", "content": PROMPT}],
    )
    return completion.choices[0].message.content


def generate_full_conspect(
    client: OpenAI, prompt: str, full_task: str, delimeter: str = "******"
) -> list[str]:
    """
    Функция использует generate_part и с помощью разделителя делит задачу на части и генерирует весь конспект по частям
    """
    result = []
    tasks_list = full_task.split(delimeter)

    parts_count = 1
    try_count = 0
    try_limit = 3

    for task in tasks_list:
        logger.info(f"Генерация части {parts_count} из {len(tasks_list)} началась")
        print(f"Генерация части {parts_count} из {len(tasks_list)} началась")
        try:
            part_result = generate_part(client, prompt, full_task, task)
            result.append(part_result)
        except Exception as e:
            print(f"Ошибка при генерации части: {e}")
            try_count += 1
            if try_count < try_limit:
                print(f"Попытка {try_count} из {try_limit}")
                logging.error(
                    f"Ошибка при генерации части: {e}. Попытка {try_count} из {try_limit}"
                )
                continue
            else:
                logging.critical(
                    f"Ошибка при генерации части: {e}. Попытка {try_count} из {try_limit}"
                )
                raise e

        else:
            parts_count += 1
            logging.info(f"Генерация части {parts_count} из {len(tasks_list)} завершена")
            continue

    return result
