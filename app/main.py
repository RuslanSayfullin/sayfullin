import os
from typing import Optional

from fastapi import FastAPI

from utils import json_to_dict_list

# Получаем путь к директории текущего скрипта
script_dir = os.path.dirname(os.path.abspath(__file__))
# Получаем путь к JSON
path_to_json = os.path.join(script_dir, 'students.json')

app = FastAPI()

@app.get("/")
def home_page():
    return {"message": "Привет, Ruslan!"}

@app.get("/students")
def get_all_students():
    return json_to_dict_list(path_to_json)