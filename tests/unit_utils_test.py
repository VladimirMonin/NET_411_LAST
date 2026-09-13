from utils.file_utils import read_file
import pytest

ASSET_READ_FILE = "tests/assets/read_file_asset.md"


def test_file_read():
    content = read_file(ASSET_READ_FILE)
    assert content == "Что такое переменная в Python?", "Содержимое не соответствует файлу"


# Проверим что появляется ошибка на чтение несуществующего файла

def test_file_read_not_found():
     with pytest.raises(FileNotFoundError):
        read_file("nonexistent_file.txt")  # Попытка прочитать несуществующий файл
