# uv add load_dotenv

from dotenv import load_dotenv
from os import getenv

load_dotenv()

POLZA_API_KEY = getenv("POLZA_API_KEY")
IS_IMAGE = getenv("IS_PAID") == "True"

