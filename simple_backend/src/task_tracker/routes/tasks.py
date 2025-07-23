import os
import requests
from fastapi import APIRouter
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("MOCKAPI_BASE_URL") + "/tasks"

router = APIRouter()


class Task(BaseModel):
    id: str | None = None
    title: str
    status: str


@router.get("/tasks", response_model=list[Task])
def get_tasks() -> list[Task]:
    response = requests.get(BASE_URL)
    response.raise_for_status()
    return response.json()


@router.post("/tasks", response_model=Task)
def create_task(task: Task) -> Task:
    response = requests.post(BASE_URL, json=task.model_dump())
    response.raise_for_status()
    return response.json()


@router.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, update_task: Task) -> Task | dict:
    url = f"{BASE_URL}/{task_id}"
    response = requests.put(url, json=update_task.model_dump())
    if response.status_code == 404:
        return {"error": "Task not found"}
    response.raise_for_status
    return response.json()


@router.delete("/tasks/{task_id}", response_model=dict)
def delete_task(task_id: str) -> dict:
    url = f"{BASE_URL}/{task_id}"
    response = requests.delete(url)
    if response.status_code == 404:
        return {"error": "Task not found"}
    response.raise_for_status
    return {"message": "Task deleted"}
