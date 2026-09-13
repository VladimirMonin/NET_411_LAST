from utils.file_utils import read_file, write_file
import pytest
import os

ASSET_READ_FILE = "tests/assets/read_file_asset.md"


def test_file_read():
    content = read_file(ASSET_READ_FILE)
    assert content == "Что такое переменная в Python?", "Содержимое не соответствует файлу"


def test_file_read_not_found():
     with pytest.raises(FileNotFoundError):
        read_file("nonexistent_file.txt")  # Попытка прочитать несуществующий файл


def test_write_file():
    content_to_write = read_file(ASSET_READ_FILE)
    write_file("test_write_file.txt", content_to_write)
    assert "test_write_file.txt" in os.listdir(), "Файл не создан"

    read_content = read_file("test_write_file.txt")
    assert read_content == content_to_write, "Содержимое файла не соответствует оригиналу"
    os.remove("test_write_file.txt")  # Удаляем созданный файл

