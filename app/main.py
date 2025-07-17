import os
from typing import Optional, List


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
def get_all_students(course: Optional[int] = None) -> List:
    students = json_to_dict_list(path_to_json)
    if course is None:
        return students
    else:
        return_list = []
        for student in students:
            if student["course"] == course:
                return_list.append(student)
        return return_list

@app.get("/students/{course}")
def get_all_students_course(course: int, major: Optional[str] = None, enrollment_year: Optional[int] = 2018) -> List:
    students = json_to_dict_list(path_to_json)
    filtered_students = []
    for student in students:
        if student["course"] == course:
            filtered_students.append(student)

        if major:
            filtered_students = [student for student in filtered_students if student['major'].lower() == major.lower()]

        if enrollment_year:
            filtered_students = [student for student in filtered_students if student['enrollment_year'] == enrollment_year]
    
    return filtered_students



