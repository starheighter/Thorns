import os
import random

DIRECTORY_PATH = "prefix/english"

def _load_prefix_modules(filename):
    try:
        with open(f"{DIRECTORY_PATH}/{filename}", "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""

def _prefix_files():
    return os.listdir(DIRECTORY_PATH)

def generate_prefix(user_message):
    prefix_files = _prefix_files()
    prefix = ""
    for file in prefix_files:
        prefix_modules = _load_prefix_modules(file).split("$")
        prefix_module = random.choice(prefix_modules)
        prefix += f"{prefix_module}\n"
    return prefix