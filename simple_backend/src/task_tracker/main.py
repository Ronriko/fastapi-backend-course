import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

BASE_URL = os.getenv("MOCKAPI_BASE_URL") + "/tasks"

app = FastAPI()


class Task(BaseModel):
    id: Optional[str] = None
    title: str
    status: str


@app.get("/tasks", response_model=list[Task])
def get_tasks():
    response = requests.get(BASE_URL)
    response.raise_for_status()
    return response.json()


@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    response = requests.post(BASE_URL, json=task.model_dump())
    response.raise_for_status()
    return response.json()


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, update_task: Task):
    url = f"{BASE_URL}/{task_id}"
    response = requests.put(url, json=update_task.model_dump())
    if response.status_code == 404:
        return {"error": "Task not found"}
    response.raise_for_status
    return response.json()


@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    url = f"{BASE_URL}/{task_id}"
    response = requests.delete(url)
    if response.status_code == 404:
        return {"error": "Task not found"}
    response.raise_for_status
    return {"message": "Task deleted"}
